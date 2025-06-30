package com.example.demo.controller;

import com.example.demo.service.EvaluacionService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Controller
@CrossOrigin(origins = "http://127.0.0.1:5000") // Permitir requests desde Flask
public class EvaluacionController {
    
    @Autowired
    private EvaluacionService evaluacionService;
    
    /**
     * Ruta raíz que redirige a evaluaciones
     */
    @GetMapping("/")
    public String index() {
        return "redirect:/evaluaciones";
    }
    
    /**
     * Página principal para mostrar actividades finalizadas
     */
    @GetMapping("/evaluaciones")
    public String mostrarEvaluaciones(Model model) {
        try {
            List<EvaluacionService.ActividadEvaluacionDTO> actividades = 
                evaluacionService.getActividadesFinalizadas();
            model.addAttribute("actividades", actividades);
            return "evaluaciones";
        } catch (Exception e) {
            model.addAttribute("error", "Error al cargar las actividades: " + e.getMessage());
            return "error";
        }
    }
    
    /**
     * API REST para agregar una nota a una actividad
     */
    @PostMapping("/api/actividades/{actividadId}/nota")
    @ResponseBody
    public ResponseEntity<Map<String, Object>> agregarNota(
            @PathVariable Long actividadId,
            @RequestBody Map<String, Integer> request) {
        
        Map<String, Object> response = new HashMap<>();
        
        try {
            Integer nota = request.get("nota");
            
            // Validación adicional en el controlador
            if (nota == null) {
                response.put("success", false);
                response.put("message", "La nota es obligatoria");
                return ResponseEntity.badRequest().body(response);
            }
            
            if (nota < 1 || nota > 7) {
                response.put("success", false);
                response.put("message", "La nota debe estar entre 1 y 7");
                return ResponseEntity.badRequest().body(response);
            }
            
            // Agregar la nota
            evaluacionService.agregarNota(actividadId, nota);
            
            // Recalcular y devolver el nuevo promedio
            String nuevoPromedio = evaluacionService.getPromedioActividad(actividadId);
            
            response.put("success", true);
            response.put("message", "Nota agregada exitosamente");
            response.put("nuevoPromedio", nuevoPromedio);
            
            return ResponseEntity.ok(response);
            
        } catch (IllegalArgumentException e) {
            response.put("success", false);
            response.put("message", e.getMessage());
            return ResponseEntity.badRequest().body(response);
        } catch (Exception e) {
            response.put("success", false);
            response.put("message", "Error interno del servidor");
            return ResponseEntity.internalServerError().body(response);
        }
    }
    
    /**
     * API para obtener el promedio actual de una actividad
     */
    @GetMapping("/api/actividades/{actividadId}/promedio")
    @ResponseBody
    public ResponseEntity<Map<String, String>> getPromedio(@PathVariable Long actividadId) {
        try {
            String promedio = evaluacionService.getPromedioActividad(actividadId);
            Map<String, String> response = new HashMap<>();
            response.put("promedio", promedio);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            Map<String, String> response = new HashMap<>();
            response.put("error", "Error al obtener el promedio");
            return ResponseEntity.internalServerError().body(response);
        }
    }
    
    /**
     * Página de error
     */
    @GetMapping("/error")
    public String error() {
        return "error";
    }
} 