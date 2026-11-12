package com.dorm.controller;
import com.dorm.common.*;
import jakarta.persistence.criteria.Predicate;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.*;
import org.springframework.data.jpa.domain.Specification;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.web.bind.annotation.*;
import java.lang.reflect.Field;
import java.util.*;
/**
 * 通用 CRUD 控制器基类：子类只需声明实体与仓库，即获得
 * 分页查询（支持任意字符串字段模糊匹配）、全量列表、详情、新增、修改、删除接口。
 */
@RequiredArgsConstructor
public abstract class CrudController<T, R extends JpaRepository<T, Long> & JpaSpecificationExecutor<T>> {
    protected final R repo;
    protected final Class<T> entityClass;

    @GetMapping
    public Result<PageResult<T>> page(@RequestParam(defaultValue = "1") int page,
                                      @RequestParam(defaultValue = "10") int size,
                                      @RequestParam Map<String, String> params) {
        Specification<T> spec = (root, q, cb) -> {
            List<Predicate> ps = new ArrayList<>();
            params.forEach((k, v) -> {
                if (v == null || v.isBlank() || k.equals("page") || k.equals("size")) return;
                try {
                    Field f = findField(entityClass, k);
                    if (f != null && f.getType() == String.class) {
                        ps.add(cb.like(root.get(k), "%" + v + "%"));
                    }
                } catch (Exception ignored) {}
            });
            return cb.and(ps.toArray(new Predicate[0]));
        };
        Page<T> p = repo.findAll(spec, PageRequest.of(page - 1, size, Sort.by(Sort.Direction.DESC, "id")));
        return Result.ok(PageResult.of(p));
    }
    private Field findField(Class<?> c, String name) {
        while (c != null) {
            try { return c.getDeclaredField(name); } catch (NoSuchFieldException e) { c = c.getSuperclass(); }
        }
        return null;
    }
    @GetMapping("/all")
    public Result<List<T>> all() { return Result.ok(repo.findAll(Sort.by(Sort.Direction.ASC, "id"))); }
    @GetMapping("/{id}")
    public Result<T> get(@PathVariable Long id) {
        return Result.ok(repo.findById(id).orElseThrow(() -> new BizException("记录不存在")));
    }
    @PostMapping
    public Result<T> create(@RequestBody T entity) { beforeSave(entity, true); return Result.ok(repo.save(entity)); }
    @PutMapping("/{id}")
    public Result<T> update(@PathVariable Long id, @RequestBody T entity) {
        if (!repo.existsById(id)) throw new BizException("记录不存在");
        setId(entity, id);
        beforeSave(entity, false);
        return Result.ok(repo.save(entity));
    }
    @DeleteMapping("/{id}")
    public Result<Void> delete(@PathVariable Long id) { repo.deleteById(id); return Result.ok(); }
    /** 子类业务校验钩子 */
    protected void beforeSave(T entity, boolean isCreate) {}
    private void setId(T entity, Long id) {
        try { Field f = findField(entityClass, "id"); f.setAccessible(true); f.set(entity, id); }
        catch (Exception ignored) {}
    }
}
