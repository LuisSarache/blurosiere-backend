#!/usr/bin/env python
"""
Script para executar todos os testes do sistema
"""
import subprocess
import sys

def run_integration_tests():
    print("🧪 Executando testes de integração...")
    result = subprocess.run([sys.executable, "test_complete.py"], capture_output=False)
    return result.returncode == 0

def run_unit_tests():
    print("\n🧪 Executando testes unitários com pytest...")
    result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"], capture_output=False)
    return result.returncode == 0

def main():
    print("="*60)
    print("🚀 EXECUTANDO SUITE COMPLETA DE TESTES")
    print("="*60)
    
    integration_passed = run_integration_tests()
    unit_passed = run_unit_tests()
    
    print("\n" + "="*60)
    print("📊 RESULTADO FINAL")
    print("="*60)
    print(f"Testes de Integração: {'✅ PASSOU' if integration_passed else '❌ FALHOU'}")
    print(f"Testes Unitários: {'✅ PASSOU' if unit_passed else '❌ FALHOU'}")
    
    if integration_passed and unit_passed:
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        return 0
    else:
        print("\n⚠️ ALGUNS TESTES FALHARAM")
        return 1

if __name__ == "__main__":
    sys.exit(main())