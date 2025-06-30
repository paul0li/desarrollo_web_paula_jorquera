package com.example.demo.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.List;

@Entity
@Table(name = "actividad")
public class Actividad {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "comuna_id", nullable = false)
    private Long comunaId;
    
    @Column(name = "sector", length = 100)
    private String sector;
    
    @Column(name = "nombre", length = 200, nullable = false)
    private String nombre;
    
    @Column(name = "email", length = 100, nullable = false)
    private String email;
    
    @Column(name = "celular", length = 15)
    private String celular;
    
    @Column(name = "dia_hora_inicio", nullable = false)
    private LocalDateTime diaHoraInicio;
    
    @Column(name = "dia_hora_termino")
    private LocalDateTime diaHoraTermino;
    
    @Column(name = "descripcion", length = 500)
    private String descripcion;
    
    // Relación con notas
    @OneToMany(mappedBy = "actividad", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Nota> notas;
    
    // Constructores
    public Actividad() {}
    
    // Getters y Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public Long getComunaId() { return comunaId; }
    public void setComunaId(Long comunaId) { this.comunaId = comunaId; }
    
    public String getSector() { return sector; }
    public void setSector(String sector) { this.sector = sector; }
    
    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }
    
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    
    public String getCelular() { return celular; }
    public void setCelular(String celular) { this.celular = celular; }
    
    public LocalDateTime getDiaHoraInicio() { return diaHoraInicio; }
    public void setDiaHoraInicio(LocalDateTime diaHoraInicio) { this.diaHoraInicio = diaHoraInicio; }
    
    public LocalDateTime getDiaHoraTermino() { return diaHoraTermino; }
    public void setDiaHoraTermino(LocalDateTime diaHoraTermino) { this.diaHoraTermino = diaHoraTermino; }
    
    public String getDescripcion() { return descripcion; }
    public void setDescripcion(String descripcion) { this.descripcion = descripcion; }
    
    public List<Nota> getNotas() { return notas; }
    public void setNotas(List<Nota> notas) { this.notas = notas; }
    
    // Método auxiliar para calcular promedio de notas
    public Double getPromedioNotas() {
        if (notas == null || notas.isEmpty()) {
            return null;
        }
        return notas.stream()
                .mapToInt(Nota::getNota)
                .average()
                .orElse(0.0);
    }
    
    // Método para verificar si la actividad está finalizada
    public boolean isFinalizat() {
        if (diaHoraTermino != null) {
            return diaHoraTermino.isBefore(LocalDateTime.now());
        }
        // Si no tiene fecha de término, consideramos que está finalizada si empezó hace más de 1 día
        return diaHoraInicio.isBefore(LocalDateTime.now().minusDays(1));
    }
} 