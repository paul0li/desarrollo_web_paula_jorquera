package com.example.demo.service;

import com.example.demo.model.Actividad;
import com.example.demo.model.ActividadTema;
import com.example.demo.model.Comuna;
import com.example.demo.model.Nota;
import com.example.demo.repository.ActividadRepository;
import com.example.demo.repository.ActividadTemaRepository;
import com.example.demo.repository.ComunaRepository;
import com.example.demo.repository.NotaRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
@Transactional
public class EvaluacionService {
    
    @Autowired
    private ActividadRepository actividadRepository;
    
    @Autowired
    private NotaRepository notaRepository;
    
    @Autowired
    private ComunaRepository comunaRepository;
    
    @Autowired
    private ActividadTemaRepository actividadTemaRepository;
    
    // DTO para transferir datos de actividades con evaluación
    public static class ActividadEvaluacionDTO {
        private Long id;
        private String fechaInicio;
        private String sector;
        private String nombre;
        private String tema;
        private String notaPromedio;
        
        // Constructor
        public ActividadEvaluacionDTO(Long id, String fechaInicio, String sector, String nombre, String tema, String notaPromedio) {
            this.id = id;
            this.fechaInicio = fechaInicio;
            this.sector = sector;
            this.nombre = nombre;
            this.tema = tema;
            this.notaPromedio = notaPromedio;
        }
        
        // Getters y Setters
        public Long getId() { return id; }
        public void setId(Long id) { this.id = id; }
        
        public String getFechaInicio() { return fechaInicio; }
        public void setFechaInicio(String fechaInicio) { this.fechaInicio = fechaInicio; }
        
        public String getSector() { return sector; }
        public void setSector(String sector) { this.sector = sector; }
        
        public String getNombre() { return nombre; }
        public void setNombre(String nombre) { this.nombre = nombre; }
        
        public String getTema() { return tema; }
        public void setTema(String tema) { this.tema = tema; }
        
        public String getNotaPromedio() { return notaPromedio; }
        public void setNotaPromedio(String notaPromedio) { this.notaPromedio = notaPromedio; }
    }
    
    /**
     * Obtiene todas las actividades finalizadas con su información para evaluación
     */
    public List<ActividadEvaluacionDTO> getActividadesFinalizadas() {
        LocalDateTime ahora = LocalDateTime.now();
        LocalDateTime fechaLimite = ahora.minusDays(1); // Para actividades sin fecha de término
        
        List<Actividad> actividades = actividadRepository.findActividadesFinalizadas(ahora, fechaLimite);
        
        // Obtener comunas en batch
        List<Long> comunaIds = actividades.stream()
                .map(Actividad::getComunaId)
                .distinct()
                .collect(Collectors.toList());
        Map<Long, Comuna> comunas = comunaRepository.findAllById(comunaIds)
                .stream()
                .collect(Collectors.toMap(Comuna::getId, comuna -> comuna));
        
        // Obtener temas en batch
        List<Long> actividadIds = actividades.stream()
                .map(Actividad::getId)
                .collect(Collectors.toList());
        Map<Long, List<ActividadTema>> temas = actividadTemaRepository.findAll()
                .stream()
                .filter(tema -> actividadIds.contains(tema.getActividadId()))
                .collect(Collectors.groupingBy(ActividadTema::getActividadId));
        
        // Obtener promedios de notas en batch
        Map<Long, Double> promedios = actividadIds.stream()
                .collect(Collectors.toMap(
                    id -> id,
                    id -> notaRepository.findPromedioByActividadId(id)
                ));
        
        List<ActividadEvaluacionDTO> resultado = new ArrayList<>();
        
        for (Actividad actividad : actividades) {
            // Sector (Comuna + sector específico)
            String sector = "";
            Comuna comuna = comunas.get(actividad.getComunaId());
            if (comuna != null) {
                sector = comuna.getNombre();
                if (actividad.getSector() != null && !actividad.getSector().trim().isEmpty()) {
                    sector += ", " + actividad.getSector();
                }
            }
            
            // Tema
            String tema = "Sin tema";
            List<ActividadTema> temasActividad = temas.get(actividad.getId());
            if (temasActividad != null && !temasActividad.isEmpty()) {
                tema = temasActividad.get(0).getNombreTema();
            }
            
            // Promedio de notas
            String notaPromedio = "-";
            Double promedio = promedios.get(actividad.getId());
            if (promedio != null) {
                notaPromedio = String.format("%.1f", promedio);
            }
            
            resultado.add(new ActividadEvaluacionDTO(
                actividad.getId(),
                actividad.getDiaHoraInicio().toString(),
                sector,
                actividad.getNombre(),
                tema,
                notaPromedio
            ));
        }
        
        return resultado;
    }
    
    /**
     * Agrega una nueva nota a una actividad
     */
    public void agregarNota(Long actividadId, Integer nota) {
        // Validar que la nota esté en el rango correcto
        if (nota < 1 || nota > 7) {
            throw new IllegalArgumentException("La nota debe estar entre 1 y 7");
        }
        
        // Verificar que la actividad existe
        if (!actividadRepository.existsById(actividadId)) {
            throw new IllegalArgumentException("La actividad no existe");
        }
        
        // Crear y guardar la nota
        Nota nuevaNota = new Nota(actividadId, nota);
        notaRepository.save(nuevaNota);
    }
    
    /**
     * Obtiene el promedio actual de una actividad
     */
    public String getPromedioActividad(Long actividadId) {
        Double promedio = notaRepository.findPromedioByActividadId(actividadId);
        if (promedio != null) {
            return String.format("%.1f", promedio);
        }
        return "-";
    }
} 