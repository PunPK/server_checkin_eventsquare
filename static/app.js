function addLog(message) {
    const log = document.getElementById("log");
    const li = document.createElement("li");
    li.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
    log.prepend(li);
}

async function checkIn() {
    const ticketId = document.getElementById("ticketId").value;
    if (!ticketId) {
        alert("กรุณาใส่ Ticket ID");
        return;
    }

    addLog(`→ ส่งคำขอ check-in: ${ticketId}`);

    try {
        const res = await fetch(`/api/tickets/check-in/${ticketId}`, {
            method: "POST"
        });

        const data = await res.json();
        document.getElementById("result").textContent =
            JSON.stringify(data, null, 2);

        addLog("✓ check-in สำเร็จ");

    } catch (err) {
        addLog("✗ error");
        document.getElementById("result").textContent = err.toString();
    }
}
