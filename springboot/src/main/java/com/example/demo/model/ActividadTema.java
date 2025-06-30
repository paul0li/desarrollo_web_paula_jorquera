package com.example.demo.model;

import jakarta.persistence.*;

@Entity
@Table(name = "actividad_tema")
public class ActividadTema {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Enumerated(EnumType.STRING)
    @Column(name = "tema", nullable = false)
    private TemaEnum tema;
    
    @Column(name = "glosa_otro", length = 15)
    private String glosaOtro;
    
    @Column(name = "actividad_id", nullable = false)
    private Long actividadId;
    
    // Enum para los temas
    public enum TemaEnum {
        música, deporte, ciencias, religión, política, tecnología, juegos, baile, comida, otro
    }
    
    // Constructores
    public ActividadTema() {}
    
    // Getters y Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public TemaEnum getTema() { return tema; }
    public void setTema(TemaEnum tema) { this.tema = tema; }
    
    public String getGlosaOtro() { return glosaOtro; }
    public void setGlosaOtro(String glosaOtro) { this.glosaOtro = glosaOtro; }
    
    public Long getActividadId() { return actividadId; }
    public void setActividadId(Long actividadId) { this.actividadId = actividadId; }
    
    // Método para obtener el nombre del tema a mostrar
    public String getNombreTema() {
        if (tema == TemaEnum.otro && glosaOtro != null && !glosaOtro.trim().isEmpty()) {
            return glosaOtro;
        }
        return tema.name();
    }
} 