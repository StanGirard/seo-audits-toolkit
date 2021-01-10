const authProviderDjango = {
    login: ({ username, password }) =>  {
        const request = new Request('http://localhost:8000/dj-rest-auth/login/', {
            method: 'POST',
            body: JSON.stringify({ username, password }),
            headers: new Headers({ 'Content-Type': 'application/json' }),
        });
        return fetch(request)
            .then(response => {
                if (response.status < 200 || response.status >= 300) {
                    throw new Error(response.statusText);
                }
                return response.json();
            })
            .then(auth => {
                localStorage.setItem('auth', JSON.stringify(auth));
            })
            .catch(() => {
                throw new Error('Network error')
            });
    },
    checkAuth: () => {
        return localStorage.getItem('auth') ? Promise.resolve() : Promise.reject();
    },
    logout: () => {
        localStorage.removeItem('auth');
        localStorage.removeItem('permissions');
        return Promise.resolve();
    },
    getPermissions: () => {
        const role = localStorage.getItem('permissions');
        return role ? Promise.resolve(role) : Promise.reject();
    },
    checkError: (error) => {
        const status = error.status;
        if (status === 401 || status === 403) {
            localStorage.removeItem('auth');
            return Promise.reject("You are not authorized to do this request");
        }
        // other error code (404, 500, etc): no need to log out
        return Promise.resolve();
    },
};

export default authProviderDjango;