const API_URL = 'http://localhost:5055/api/blog';

export async function getAllPosts() {
    const res = await fetch(API_URL + '/posts', { method: 'GET' });
    if (!res.ok) {
        const data = await res.json()
        const msg = data.msg || 'Network response was not ok';
        throw new Error(msg);
    }
    return await res.json();
}

export async function createPost(post) {
    const res = await fetch(API_URL + '/post', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(post),
    });
    if (!res.ok) {
        const data = await res.json()
        const msg = data.msg || 'Network response was not ok';
        throw new Error(msg);
    }
    return await res.json();
}

export async function deletePost(id) {
    const params = new URLSearchParams({ id });
    const url = new URL(API_URL + '/post' + '?' + params);
    const res = await fetch(url, {
        method: 'DELETE',
    });
    if (!res.ok) {
        const data = await res.json()
        const msg = data.msg || 'Network response was not ok';
        throw new Error(msg);
    }
    return await res.json();
}

export async function updatePost(post) {
    const res = await fetch(API_URL + '/post', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(post),
    });
    if (!res.ok) {
        const data = await res.json()
        const msg = data.msg || 'Network response was not ok';
        throw new Error(msg);
    }
    return await res.json();
}

export async function getPost(id) {
    const params = new URLSearchParams({ id });
    const url = new URL(API_URL + '/post' + '?' + params);
    const res = await fetch(url, {
        method: 'GET',
    });
    if (!res.ok) {
        const data = await res.json()
        const msg = data.msg || 'Network response was not ok';
        throw new Error(msg);
    }
    return await res.json();
}