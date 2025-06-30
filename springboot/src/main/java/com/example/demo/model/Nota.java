package com.example.demo.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;

@Entity
@Table(name = "nota")
public class Nota {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "actividad_id", nullable = false)
    private Long actividadId;
    
    @NotNull(message = "La nota es obligatoria")
    @Min(value = 1, message = "La nota debe ser mínimo 1")
    @Max(value = 7, message = "La nota debe ser máximo 7")
    @Column(name = "nota", nullable = false)
    private Integer nota;
    
    // Relación con actividad
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "actividad_id", insertable = false, updatable = false)
    private Actividad actividad;
    
    // Constructores
    public Nota() {}
    
    public Nota(Long actividadId, Integer nota) {
        this.actividadId = actividadId;
        this.nota = nota;
    }
    
    // Getters y Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public Long getActividadId() { return actividadId; }
    public void setActividadId(Long actividadId) { this.actividadId = actividadId; }
    
    public Integer getNota() { return nota; }
    public void setNota(Integer nota) { this.nota = nota; }
    
    public Actividad getActividad() { return actividad; }
    public void setActividad(Actividad actividad) { this.actividad = actividad; }
} 