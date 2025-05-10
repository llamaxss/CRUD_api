const API_URL = 'http://localhost:5055/api/chat'

export async function loginHandle(username, password) {
    const res = await fetch(API_URL + '/auth', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
        credentials: "include",
    });

    if (!res.ok) {
        const data = await res.json();

        const errorMessage = data.error || "Auth failed";

        throw new Error(errorMessage)
    };

    return await res.json();
}

export async function logOutHandle() {
    const res = await fetch(API_URL + "/logout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
    });

    if (!res.ok) {
        const data = await res.json();

        const errorMessage = data.error || "Logout failed";

        throw new Error(errorMessage)
    }

    return await res.json();
}

export async function registerHandle(username, password) {
    const res = await fetch(API_URL + '/register', {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
        credentials: "include",
    });

    if (!res.ok) {
        const data = await res.json();

        const errorMessage = data.error || "Register failed";

        throw new Error(errorMessage)
    }

    return await res.json();
}