const API_URL = 'http://localhost:5055/api';

export async function getWetherbyCityName(cityName) {
    const params = new URLSearchParams({
        cityName
    });
    const res = await fetch(API_URL + '/weather/city' + '?' + params, { method: 'GET' });

    if (!res.ok) {
        const data = await res.json()
        const msg = data.error || 'Network response was not ok';
        throw new Error(msg);
    }
    return await res.json();
}

export async function getWetherbyGeoCode(lat, lon) {
    const params = new URLSearchParams({
        lat,
        lon
    });
    const res = await fetch(API_URL + '/weather/geocode' + '?' + params, { method: 'GET' });
    if (!res.ok) {
        const data = await res.json()
        const msg = data.error || 'Network response was not ok';
        throw new Error(msg);
    }
    return await res.json();
}
