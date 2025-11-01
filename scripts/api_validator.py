"""
Script para validar el comportamiento de endpoints de la API mediante múltiples peticiones.
Genera estadísticas de rendimiento, tasa de éxito/error y tiempos de respuesta.
"""

import asyncio
import aiohttp
import time
from typing import List, Dict, Any
from dataclasses import dataclass, field
from statistics import mean, median, stdev
import json
from datetime import datetime


@dataclass
class RequestResult:
    """Resultado de una petición individual"""
    success: bool
    status_code: int
    response_time: float
    error: str = ""
    response_data: Dict = field(default_factory=dict)


@dataclass
class ValidationReport:
    """Reporte completo de validación"""
    endpoint: str
    total_requests: int
    successful_requests: int
    failed_requests: int
    avg_response_time: float
    min_response_time: float
    max_response_time: float
    median_response_time: float
    std_dev_response_time: float
    requests_per_second: float
    status_codes: Dict[int, int]
    errors: List[str]
    duration: float


class APIValidator:
    """Validador de endpoints de API con capacidad de pruebas de carga"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results: List[RequestResult] = []

    async def make_request(
        self,
        session: aiohttp.ClientSession,
        method: str,
        endpoint: str,
        data: Dict = None,
        headers: Dict = None
    ) -> RequestResult:
        """Realizar una petición HTTP y registrar el resultado"""
        url = f"{self.base_url}{endpoint}"
        start_time = time.time()
        
        try:
            async with session.request(
                method=method,
                url=url,
                json=data,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                response_time = time.time() - start_time
                
                try:
                    response_data = await response.json()
                except:
                    response_data = {"text": await response.text()}
                
                return RequestResult(
                    success=response.status < 400,
                    status_code=response.status,
                    response_time=response_time,
                    response_data=response_data
                )
        
        except Exception as e:
            response_time = time.time() - start_time
            return RequestResult(
                success=False,
                status_code=0,
                response_time=response_time,
                error=str(e)
            )
    
    async def validate_endpoint(
        self,
        endpoint: str,
        method: str = "GET",
        num_requests: int = 100,
        concurrent: int = 10,
        data: Dict = None,
        headers: Dict = None
    ) -> ValidationReport:
        """
        Validar un endpoint con múltiples peticiones concurrentes
        
        Args:
            endpoint: Ruta del endpoint (ej: "/health")
            method: Método HTTP (GET, POST, etc.)
            num_requests: Número total de peticiones a realizar
            concurrent: Número de peticiones concurrentes
            data: Datos a enviar en peticiones POST/PUT
            headers: Headers personalizados
        """
        print(f"\n{'='*70}")
        print(f"Iniciando validación de: {method} {endpoint}")
        print(f"Peticiones totales: {num_requests}")
        print(f"Concurrencia: {concurrent}")
        print(f"{'='*70}\n")
        
        self.results = []
        start_time = time.time()
        
        connector = aiohttp.TCPConnector(limit=concurrent)
        async with aiohttp.ClientSession(connector=connector) as session:
            # Dividir peticiones en lotes concurrentes
            for i in range(0, num_requests, concurrent):
                batch_size = min(concurrent, num_requests - i)
                tasks = [
                    self.make_request(session, method, endpoint, data, headers)
                    for _ in range(batch_size)
                ]
                batch_results = await asyncio.gather(*tasks)
                self.results.extend(batch_results)

                # Mostrar progreso
                progress = (i + batch_size) / num_requests * 100
                print(f"Progreso: {progress:.1f}% ({i + batch_size}/{num_requests})", end='\r')
        
        total_duration = time.time() - start_time
        print(f"\nCompletado en {total_duration:.2f} segundos\n")
        
        return self._generate_report(endpoint, total_duration)
    
    def _generate_report(self, endpoint: str, duration: float) -> ValidationReport:
        """Generar reporte de validación"""
        successful = [r for r in self.results if r.success]
        failed = [r for r in self.results if not r.success]
        
        response_times = [r.response_time for r in self.results]
        status_codes = {}
        errors = []
        
        for result in self.results:
            status_codes[result.status_code] = status_codes.get(result.status_code, 0) + 1
            if result.error:
                errors.append(result.error)
        
        report = ValidationReport(
            endpoint=endpoint,
            total_requests=len(self.results),
            successful_requests=len(successful),
            failed_requests=len(failed),
            avg_response_time=mean(response_times) if response_times else 0,
            min_response_time=min(response_times) if response_times else 0,
            max_response_time=max(response_times) if response_times else 0,
            median_response_time=median(response_times) if response_times else 0,
            std_dev_response_time=stdev(response_times) if len(response_times) > 1 else 0,
            requests_per_second=len(self.results) / duration if duration > 0 else 0,
            status_codes=status_codes,
            errors=list(set(errors)),
            duration=duration
        )
        
        self._print_report(report)
        return report
    
    def _print_report(self, report: ValidationReport):
        """Imprimir reporte formateado"""
        print(f"\n{'='*70}")
        print(f"REPORTE DE VALIDACIÓN - {report.endpoint}")
        print(f"{'='*70}\n")
        
        print(f"📊 RESUMEN GENERAL:")
        print(f"  • Total de peticiones: {report.total_requests}")
        print(f"  • Exitosas: {report.successful_requests} ({report.successful_requests/report.total_requests*100:.1f}%)")
        print(f"  • Fallidas: {report.failed_requests} ({report.failed_requests/report.total_requests*100:.1f}%)")
        print(f"  • Duración total: {report.duration:.2f}s")
        print(f"  • Peticiones/segundo: {report.requests_per_second:.2f}")
        
        print(f"\n⏱️  TIEMPOS DE RESPUESTA:")
        print(f"  • Promedio: {report.avg_response_time*1000:.2f}ms")
        print(f"  • Mediana: {report.median_response_time*1000:.2f}ms")
        print(f"  • Mínimo: {report.min_response_time*1000:.2f}ms")
        print(f"  • Máximo: {report.max_response_time*1000:.2f}ms")
        print(f"  • Desv. Estándar: {report.std_dev_response_time*1000:.2f}ms")
        
        print(f"\n📈 CÓDIGOS DE ESTADO:")
        for code, count in sorted(report.status_codes.items()):
            percentage = count / report.total_requests * 100
            print(f"  • {code}: {count} ({percentage:.1f}%)")
        
        if report.errors:
            print(f"\n❌ ERRORES ENCONTRADOS:")
            for error in report.errors[:5]:  # Mostrar solo primeros 5
                print(f"  • {error}")
            if len(report.errors) > 5:
                print(f"  • ... y {len(report.errors) - 5} errores más")
        
        print(f"\n{'='*70}\n")
    
    def save_report(self, report: ValidationReport, filename: str = None):
        """Guardar reporte en archivo JSON"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"validation_report_{timestamp}.json"
        
        report_dict = {
            "endpoint": report.endpoint,
            "timestamp": datetime.now().isoformat(),
            "total_requests": report.total_requests,
            "successful_requests": report.successful_requests,
            "failed_requests": report.failed_requests,
            "avg_response_time_ms": report.avg_response_time * 1000,
            "min_response_time_ms": report.min_response_time * 1000,
            "max_response_time_ms": report.max_response_time * 1000,
            "median_response_time_ms": report.median_response_time * 1000,
            "std_dev_response_time_ms": report.std_dev_response_time * 1000,
            "requests_per_second": report.requests_per_second,
            "duration_seconds": report.duration,
            "status_codes": report.status_codes,
            "errors": report.errors
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_dict, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Reporte guardado en: {filename}")

import os
# cargar .env
from dotenv import load_dotenv
load_dotenv(
    override=True,
)

async def main():
    """Ejemplo de uso del validador"""
    # variable de entorno API_BASE_URL puede ser usada para cambiar la URL base
    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
    print(f"Usando API_BASE_URL: {API_BASE_URL}")
    validator = APIValidator(base_url=API_BASE_URL)
    
    # Test 1: Health endpoint
    print("\n🏥 TEST 1: Health Check")
    report_health = await validator.validate_endpoint(
        endpoint="/health",
        method="GET",
        num_requests=200,
        concurrent=20
    )
    validator.save_report(report_health, "report_health.json")

    # Test 2: Info endpoint
    print("\n📝 TEST 2: Model Info")
    report_info = await validator.validate_endpoint(
        endpoint="/info",
        method="GET",
        num_requests=500,
        concurrent=100
    )
    validator.save_report(report_info, "report_info.json")
    # Test 3: Predict endpoint
    print("\n🔮 TEST 3: Predictions")
    prediction_data = {
        "features": [5.1, 3.5, 1.4, 0.2]
    }
    report_predict = await validator.validate_endpoint(
        endpoint="/predict",
        method="POST",
        num_requests=500,
        concurrent=100,
        data=prediction_data
    )
    validator.save_report(report_predict, "report_predict.json")
    # Test 4: Endpoint no existente (404)
    print("\n🚫 TEST 4: Endpoint No Existente")
    report_404 = await validator.validate_endpoint(
        endpoint="/nonexistent",
        method="GET",
        num_requests=400,
        concurrent=100
    )
    validator.save_report(report_404, "report_404.json")


if __name__ == "__main__":
    asyncio.run(main())