// frontend/src/index.tsx
import { customElement } from 'solid-element';
import { createSignal, createEffect, onCleanup, For } from 'solid-js';

// カスタムエレメントの定義と登録
customElement(
  'solid-chat', // HTMLで使うタグ名: <solid-chat>
  { username: 'Guest', wsUrl: '' }, // 属性（プロパティ）の初期値（キャメルケースで定義すると、HTML側ではケバブケース `ws-url` になります）
  (props) => {
    const [messages, setMessages] = createSignal<{ user: string; text: string }[]>([]);
    const [inputText, setInputText] = createSignal('');
    let ws: WebSocket | null = null;

    // wsUrl または username が変更・確定したタイミングでWebSocketを初期化
    createEffect(() => {
      if (!props.wsUrl) return;

      ws = new WebSocket(props.wsUrl);

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        setMessages((prev) => [...prev, data]);
      };

      // コンポーネント（要素）がドムから削除されたらクローズ
      onCleanup(() => {
        if (ws) ws.close();
      });
    });

    const sendMessage = (e: Event) => {
      e.preventDefault();
      if (!inputText().trim() || !ws) return;

      ws.send(inputText());
      setInputText('');
    };

    return (
      <div style={{ padding: '20px', "max-width": '500px', border: '1px solid #ddd', "border-radius": '8px', "background-color": '#fafafa' }}>
        <h3>こんにちは、{props.username} さん (Web Component)</h3>
        
        {/* メッセージエリア */}
        <div style={{ border: '1px solid #ccc', "background-color": '#fff', height: '250px', "overflow-y": 'auto', padding: '10px', "margin-bottom": '10px' }}>
          <For each={messages()}>
            {(msg) => (
              <div style={{ "margin-bottom": '8px' }}>
                <strong>{msg.user}:</strong> <span>{msg.text}</span>
              </div>
            )}
          </For>
        </div>

        {/* フォーム */}
        <form onSubmit={sendMessage} style={{ display: 'flex', gap: '8px' }}>
          <input
            type="text"
            value={inputText()}
            onInput={(e) => setInputText(e.currentTarget.value)}
            placeholder="メッセージを入力..."
            style={{ flex: 1, padding: '8px' }}
          />
          <button type="submit" style={{ padding: '8px 16px', "background-color": '#007bff', color: '#fff', border: 'none', "border-radius": '4px', cursor: 'pointer' }}>
            送信
          </button>
        </form>
      </div>
    );
  }
);

