package com.example.demo.repository;

import com.example.demo.model.Actividad;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;

@Repository
public interface ActividadRepository extends JpaRepository<Actividad, Long> {
    
    // Actividades finalizadas (fecha de término anterior a la actual)
    @Query("SELECT a FROM Actividad a WHERE a.diaHoraTermino < :fechaActual OR (a.diaHoraTermino IS NULL AND a.diaHoraInicio < :fechaLimite) ORDER BY a.diaHoraInicio DESC")
    List<Actividad> findActividadesFinalizadas(LocalDateTime fechaActual, LocalDateTime fechaLimite);
    
    // Actividades finalizadas con información de promedio de notas
    @Query("""
        SELECT a, 
               CASE WHEN COUNT(n) > 0 THEN AVG(CAST(n.nota AS double)) ELSE NULL END as promedio
        FROM Actividad a 
        LEFT JOIN a.notas n 
        WHERE a.diaHoraTermino < :fechaActual 
           OR (a.diaHoraTermino IS NULL AND a.diaHoraInicio < :fechaLimite)
        GROUP BY a 
        ORDER BY a.diaHoraInicio DESC
        """)
    List<Object[]> findActividadesFinalizadasConPromedio(LocalDateTime fechaActual, LocalDateTime fechaLimite);
} 