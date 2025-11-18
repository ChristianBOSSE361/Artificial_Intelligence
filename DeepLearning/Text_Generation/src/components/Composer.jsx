//Text box and "Enter" or send button
import React, { useState } from "react";

export default function Composer({ onSend, disabled }){
    const [query, setquery]= useState("");

    const handleChange = (e) => {
        setquery(e);
    };

    return (
        <div className="composer">
            <textarea
                type="query"
                value={query}
                onchange= {handleChange}
                placeholder="How can I help you today?"
            />
            <button>
                onClick={()=> {onSend(query); setquery("");} }
                disabled={!text.trim() || disabled}
            </button>
        </div>
    )
}