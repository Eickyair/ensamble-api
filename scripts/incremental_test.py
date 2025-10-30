"""
Script de pruebas de estrés para la API.
Incrementa gradualmente la carga para encontrar límites de rendimiento.
"""

import asyncio
import aiohttp
import time
from typing import List, Tuple
import matplotlib.pyplot as plt
from dataclasses import dataclass


@dataclass
class StressTestResult:
    """Resultado de prueba de estrés"""
    concurrent_users: int
    requests_per_second: float
    avg_response_time: float
    error_rate: float
    successful_requests: int
    failed_requests: int


class StressTester:
    """Realizador de pruebas de estrés incrementales"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results: List[StressTestResult] = []
    
    async def run_load_test(
        self,
        endpoint: str,
        method: str,
        concurrent_users: int,
        duration_seconds: int = 10,
        data: dict = None
    ) -> StressTestResult:
        """Ejecutar test de carga con un nivel de concurrencia específico"""
        print(f"\n🔥 Probando con {concurrent_users} usuarios concurrentes...")
        results = []
        start_time = time.time()
        end_time = start_time + duration_seconds

        async def make_requests():
            """Hacer peticiones continuamente durante la duración especificada"""
            connector = aiohttp.TCPConnector(limit=concurrent_users)
            async with aiohttp.ClientSession(connector=connector) as session:
                while time.time() < end_time:
                    tasks = []
                    for _ in range(concurrent_users):
                        url = f"{self.base_url}{endpoint}"
                        task = asyncio.create_task(self._single_request(session, method, url, data))
                        tasks.append(task)
                    batch_results = await asyncio.gather(*tasks, return_exceptions=True)
                    results.extend([r for r in batch_results if not isinstance(r, Exception)])
        await make_requests()
        actual_duration = time.time() - start_time
        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]
        response_times = [r['response_time'] for r in results if 'response_time' in r]
        result = StressTestResult(
            concurrent_users=concurrent_users,
            requests_per_second=len(results) / actual_duration,
            avg_response_time=sum(response_times) / len(response_times) if response_times else 0,
            error_rate=len(failed) / len(results) if results else 0,
            successful_requests=len(successful),
            failed_requests=len(failed)
        )

        self._print_result(result)
        return result
    async def _single_request(self, session, method, url, data):
        """Realizar una petición individual"""
        start = time.time()
        try:
            async with session.request(
                method=method,
                url=url,
                json=data,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                await response.read()
                return {
                    'success': response.status < 400,
                    'response_time': time.time() - start,
                    'status': response.status
                }
        except Exception as e:
            return {
                'success': False,
                'response_time': time.time() - start,
                'error': str(e)
            }
    
    def _print_result(self, result: StressTestResult):
        """Imprimir resultado de un test"""
        print(f"  ✓ RPS: {result.requests_per_second:.2f}")
        print(f"  ✓ Tiempo promedio: {result.avg_response_time*1000:.2f}ms")
        print(f"  ✓ Tasa de error: {result.error_rate*100:.2f}%")
        print(f"  ✓ Exitosas: {result.successful_requests}, Fallidas: {result.failed_requests}")
    
    async def run_stress_test(
        self,
        endpoint: str,
        method: str = "GET",
        data: dict = None,
        start_users: int = 10,
        max_users: int = 200,
        step: int = 20,
        duration_per_level: int = 10
    ):
        """
        Ejecutar prueba de estrés incremental
        
        Args:
            endpoint: Endpoint a probar
            method: Método HTTP
            data: Datos para POST/PUT
            start_users: Usuarios concurrentes iniciales
            max_users: Usuarios concurrentes máximos
            step: Incremento de usuarios entre niveles
            duration_per_level: Duración de cada nivel en segundos
        """
        print(f"\n{'='*70}")
        print(f"PRUEBA DE ESTRÉS INCREMENTAL")
        print(f"Endpoint: {method} {endpoint}")
        print(f"Usuarios: {start_users} → {max_users} (paso {step})")
        print(f"Duración por nivel: {duration_per_level}s")
        print(f"{'='*70}")
        
        self.results = []
        
        for concurrent_users in range(start_users, max_users + 1, step):
            result = await self.run_load_test(
                endpoint=endpoint,
                method=method,
                concurrent_users=concurrent_users,
                duration_seconds=duration_per_level,
                data=data
            )
            self.results.append(result)
            
            # Pausa entre niveles
            await asyncio.sleep(2)
        
        self._plot_results()
        self._print_summary()
    
    def _plot_results(self):
        """Generar gráficos de resultados"""
        if not self.results:
            return
        
        users = [r.concurrent_users for r in self.results]
        rps = [r.requests_per_second for r in self.results]
        response_times = [r.avg_response_time * 1000 for r in self.results]
        error_rates = [r.error_rate * 100 for r in self.results]
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
        
        # RPS
        ax1.plot(users, rps, marker='o', linewidth=2, markersize=8)
        ax1.set_xlabel('Usuarios Concurrentes')
        ax1.set_ylabel('Peticiones por Segundo')
        ax1.set_title('Throughput vs Concurrencia')
        ax1.grid(True, alpha=0.3)
        
        # Tiempo de respuesta
        ax2.plot(users, response_times, marker='s', color='orange', linewidth=2, markersize=8)
        ax2.set_xlabel('Usuarios Concurrentes')
        ax2.set_ylabel('Tiempo de Respuesta (ms)')
        ax2.set_title('Latencia vs Concurrencia')
        ax2.grid(True, alpha=0.3)
        
        # Tasa de error
        ax3.plot(users, error_rates, marker='^', color='red', linewidth=2, markersize=8)
        ax3.set_xlabel('Usuarios Concurrentes')
        ax3.set_ylabel('Tasa de Error (%)')
        ax3.set_title('Errores vs Concurrencia')
        ax3.grid(True, alpha=0.3)
        
        # Comparación RPS vs Latencia
        ax4_twin = ax4.twinx()
        ax4.plot(users, rps, marker='o', label='RPS', linewidth=2)
        ax4_twin.plot(users, response_times, marker='s', color='orange', label='Latencia', linewidth=2)
        ax4.set_xlabel('Usuarios Concurrentes')
        ax4.set_ylabel('Peticiones por Segundo', color='blue')
        ax4_twin.set_ylabel('Tiempo de Respuesta (ms)', color='orange')
        ax4.set_title('RPS y Latencia Combined')
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        filename = f"stress_test_{int(time.time())}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"\n📊 Gráfico guardado: {filename}")
        plt.close()
    
    def _print_summary(self):
        """Imprimir resumen de resultados"""
        if not self.results:
            return
        
        print(f"\n{'='*70}")
        print("RESUMEN DE PRUEBA DE ESTRÉS")
        print(f"{'='*70}\n")
        
        max_rps = max(self.results, key=lambda r: r.requests_per_second)
        min_latency = min(self.results, key=lambda r: r.avg_response_time)
        first_errors = next((r for r in self.results if r.error_rate > 0.01), None)
        
        print(f"🏆 Mejor throughput:")
        print(f"   {max_rps.requests_per_second:.2f} RPS con {max_rps.concurrent_users} usuarios")
        
        print(f"\n⚡ Mejor latencia:")
        print(f"   {min_latency.avg_response_time*1000:.2f}ms con {min_latency.concurrent_users} usuarios")
        
        if first_errors:
            print(f"\n⚠️  Primeros errores:")
            print(f"   Con {first_errors.concurrent_users} usuarios ({first_errors.error_rate*100:.2f}% errores)")
        else:
            print(f"\n✅ Sin errores detectados en ningún nivel")
        
        print(f"\n{'='*70}\n")

import os
from dotenv import load_dotenv
load_dotenv(
    override=True
)
async def main():
    """Ejecutar pruebas de estrés"""
    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
    tester = StressTester(base_url=API_BASE_URL)

    # Test de predicción con carga incremental
    prediction_data = {"features": [5.1, 3.5, 1.4, 0.2]}

    await tester.run_stress_test(
        endpoint="/predict",
        method="POST",
        data=prediction_data,
        start_users=100,
        max_users=300, # 300 usuarios concurrentes durante 100 segundos
        step=100,
        duration_per_level=10
    )


if __name__ == "__main__":
    asyncio.run(main())