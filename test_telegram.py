#!/usr/bin/env python3
import requests
import json

def send_telegram_message(message):
    try:
        bot_token = "8218411510:AAH9xMjWe8eJNa7APgaOvP9aXiuf8j86OA8"
        chat_id = None
        
        # Primeiro, tenta obter o chat_id das atualizações recentes
        try:
            updates_url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
            response = requests.get(updates_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data['ok'] and data['result']:
                    # Pega o último chat_id disponível
                    for update in reversed(data['result']):  # Começa pelo mais recente
                        if 'message' in update:
                            chat_id = update['message']['chat']['id']
                            break
        except Exception as e:
            print(f"Erro ao buscar updates: {e}")
            pass
        
        # Se não conseguiu obter o chat_id das atualizações, usa arquivo de config
        if chat_id is None:
            try:
                with open('telegram_config.json', 'r') as f:
                    config = json.load(f)
                    chat_id = config.get('chat_id')
            except:
                print("Arquivo de configuração não encontrado.")
                print("Para receber notificações, envie qualquer mensagem para o bot @brd2025bot primeiro")
                return False
        
        if chat_id:
            send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': message
            }
            
            response = requests.post(send_url, json=payload, timeout=10)
            if response.status_code == 200:
                print(f"Mensagem enviada com sucesso para chat_id: {chat_id}")
                # Salva o chat_id para uso futuro
                try:
                    with open('telegram_config.json', 'w') as f:
                        json.dump({'chat_id': chat_id}, f)
                    print("Chat ID salvo no arquivo telegram_config.json")
                except:
                    pass
                return True
            else:
                print(f"Erro ao enviar mensagem. Status: {response.status_code}")
                print(f"Resposta: {response.text}")
        else:
            print("Chat ID não encontrado.")
            print("Para receber notificações, envie qualquer mensagem para o bot @brd2025bot primeiro")
        
        return False
        
    except Exception as e:
        print(f"Erro ao enviar mensagem para Telegram: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testando envio de mensagem para Telegram...")
    print("Verificando se existe algum chat disponível...")
    
    # Testa a função
    success = send_telegram_message("Teste: saiu da fila")
    
    if success:
        print("✅ Teste realizado com sucesso!")
    else:
        print("❌ Teste falhou.")
        print("\nPara configurar:")
        print("1. Abra o Telegram")
        print("2. Busque por @brd2025bot")
        print("3. Envie qualquer mensagem (ex: /start)")
        print("4. Execute este teste novamente")