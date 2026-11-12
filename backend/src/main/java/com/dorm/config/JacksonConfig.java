package com.dorm.config;
import com.fasterxml.jackson.core.JsonParser;
import com.fasterxml.jackson.databind.DeserializationContext;
import com.fasterxml.jackson.databind.deser.std.StdDeserializer;
import com.fasterxml.jackson.databind.module.SimpleModule;
import com.fasterxml.jackson.datatype.jsr310.ser.LocalDateTimeSerializer;
import org.springframework.boot.autoconfigure.jackson.Jackson2ObjectMapperBuilderCustomizer;
import org.springframework.context.annotation.*;
import java.io.IOException;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
/** 统一时间格式：LocalDateTime 序列化为 yyyy-MM-dd HH:mm:ss；反序列化兼容空格与 T 两种分隔符 */
@Configuration
public class JacksonConfig {
    static final DateTimeFormatter FMT = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
    static class FlexibleLdtDeserializer extends StdDeserializer<LocalDateTime> {
        FlexibleLdtDeserializer() { super(LocalDateTime.class); }
        @Override
        public LocalDateTime deserialize(JsonParser p, DeserializationContext ctx) throws IOException {
            String s = p.getValueAsString().trim();
            try { return LocalDateTime.parse(s); }
            catch (Exception e) { return LocalDateTime.parse(s, FMT); }
        }
    }
    @Bean
    public Jackson2ObjectMapperBuilderCustomizer ldtCustomizer() {
        return builder -> {
            SimpleModule m = new SimpleModule();
            m.addSerializer(LocalDateTime.class, new LocalDateTimeSerializer(FMT));
            m.addDeserializer(LocalDateTime.class, new FlexibleLdtDeserializer());
            builder.modulesToInstall(m);
        };
    }
}
