const BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";

export async function sendQuestion(question) {
  const res = await fetch(`${BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json(); // { answer: "...", sources: [...] }
}