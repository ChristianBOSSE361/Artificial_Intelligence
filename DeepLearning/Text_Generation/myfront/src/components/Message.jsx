export default function Message({ msg }) {
  return (
    <div className={`message ${msg.role}`}>
      <div className="text" dangerouslySetInnerHTML={{__html: msg.text}} />
      {msg.sources && msg.sources.length > 0 && (
        <div className="sources">
          {msg.sources.map((s, i) => (
            <div key={i} className="source">[Source {s.id}] {s.text?.slice(0,150)}...</div>
          ))}
        </div>
      )}
    </div>
    )
}