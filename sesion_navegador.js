const encoder = new TextEncoder();
const context = "gestionrap-session:v1:";
let opening;

function database() {
    if (!opening) {
        opening = new Promise((resolve, reject) => {
            const request = indexedDB.open("gestionrap-session", 1);
            request.onupgradeneeded = () => request.result.createObjectStore("sessions");
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
            request.onblocked = () => reject(new Error("IndexedDB is blocked"));
        });
    }
    return opening;
}

async function stored(mode, operation) {
    const db = await database();
    return new Promise((resolve, reject) => {
        const transaction = db.transaction("sessions", mode);
        const request = operation(transaction.objectStore("sessions"));
        transaction.oncomplete = () => resolve(request.result);
        transaction.onabort = () => reject(transaction.error);
        transaction.onerror = () => reject(transaction.error);
    });
}

function encode(buffer) {
    return btoa(String.fromCharCode(...new Uint8Array(buffer)));
}

async function enroll(id) {
    const params = {name: "ECDSA", namedCurve: "P-256"};
    const pair = await crypto.subtle.generateKey(params, false, ["sign", "verify"]);
    const publicKey = encode(await crypto.subtle.exportKey("raw", pair.publicKey));
    await stored("readwrite", store => store.put({id, key: pair.privateKey}, "session"));
    return {id, publicKey};
}

async function restore(challenge) {
    const record = await stored("readonly", store => store.get("session"));
    if (!record) return null;
    const proof = await crypto.subtle.sign(
        {name: "ECDSA", hash: "SHA-256"}, record.key, encoder.encode(context + challenge),
    );
    return {id: record.id, proof: encode(proof)};
}

async function revoke(id) {
    const db = await database();
    const transaction = db.transaction("sessions", "readwrite");
    const store = transaction.objectStore("sessions");
    const request = store.get("session");
    request.onsuccess = () => {
        if (request.result?.id === id) store.delete("session");
    };
}

export default function ({data, parentElement, setTriggerValue}) {
    const root = parentElement.querySelector("span");
    const operation = data.enroll || data.challenge || data.revoke;
    if (!operation || root.dataset.operation === operation) return;
    root.dataset.operation = operation;
    if (data.revoke) {
        revoke(data.revoke).catch(() => {});
        return;
    }
    const task = data.enroll ? enroll(data.enroll) : restore(data.challenge);
    task.then(result => {
        if (!result) return;
        if (data.challenge) {
            const form = document.querySelector(".st-key-rap-login-form [data-testid=stForm]");
            if (form?.contains(document.activeElement) ||
                [...(form?.querySelectorAll("input") || [])].some(input => input.value)) return;
        }
        setTriggerValue("reply", {operation, result});
    }).catch(() => {});
}
