#!/usr/bin/env python3
import requests
import json

def get_chat_id_by_phone():
    """
    Método alternativo para configurar o Telegram usando o token do bot
    """
    bot_token = "8218411510:AAH9xMjWe8eJNa7APgaOvP9aXiuf8j86OA8"
    
    print("Configurando Telegram para notificações...")
    print("1. Abra o Telegram no seu celular")
    print("2. Busque por @brd2025bot")
    print("3. Envie qualquer mensagem para o bot (ex: /start ou 'oi')")
    input("4. Pressione Enter depois de enviar a mensagem...")
    
    # Busca por updates recentes
    try:
        updates_url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
        response = requests.get(updates_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data['ok'] and data['result']:
                print("\nMensagens encontradas:")
                
                # Mostra todas as conversas encontradas
                chats = {}
                for update in data['result']:
                    if 'message' in update:
                        chat_id = update['message']['chat']['id']
                        username = update['message']['chat'].get('username', 'N/A')
                        first_name = update['message']['chat'].get('first_name', 'N/A')
                        text = update['message'].get('text', 'N/A')
                        
                        chats[chat_id] = {
                            'username': username,
                            'first_name': first_name,
                            'last_text': text
                        }
                
                if chats:
                    print("\nChats encontrados:")
                    for i, (chat_id, info) in enumerate(chats.items(), 1):
                        print(f"{i}. Chat ID: {chat_id}")
                        print(f"   Nome: {info['first_name']}")
                        print(f"   Username: @{info['username']}")
                        print(f"   Última mensagem: {info['last_text']}")
                        print()
                    
                    # Use o chat mais recente
                    latest_chat_id = list(chats.keys())[-1]
                    
                    # Salva a configuração
                    config = {'chat_id': latest_chat_id}
                    with open('telegram_config.json', 'w') as f:
                        json.dump(config, f, indent=2)
                    
                    print(f"✅ Chat ID {latest_chat_id} configurado com sucesso!")
                    
                    # Testa enviando uma mensagem
                    test_message = "🔔 Notificações do Auto-Login configuradas com sucesso!"
                    send_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                    payload = {
                        'chat_id': latest_chat_id,
                        'text': test_message
                    }
                    
                    test_response = requests.post(send_url, json=payload, timeout=10)
                    if test_response.status_code == 200:
                        print("✅ Mensagem de teste enviada com sucesso!")
                        print("Agora você receberá notificações quando sair da fila.")
                        return True
                    else:
                        print(f"❌ Erro ao enviar mensagem de teste: {test_response.text}")
                else:
                    print("❌ Nenhum chat encontrado.")
            else:
                print("❌ Nenhuma mensagem encontrada.")
                print("Certifique-se de ter enviado uma mensagem para o bot.")
        else:
            print(f"❌ Erro na API: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro: {str(e)}")
    
    return False

if __name__ == "__main__":
    success = get_chat_id_by_phone()
    
    if success:
        print("\n🎉 Configuração concluída!")
        print("O sistema agora enviará 'saiu da fila' quando detectar que saiu da fila.")
    else:
        print("\n❌ Configuração falhou.")
        print("Tente novamente seguindo as instruções.")