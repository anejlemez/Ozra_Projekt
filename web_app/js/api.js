const Api = {
    async request(endpoint, options = {}) {
        const url = `${CONFIG.API_BASE_URL}${endpoint}`;

        try {
            const response = await fetch(url, options);

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error("API napaka:", error);
            throw error;
        }
    },

    getTekmovanja() {
        return this.request("/tekmovanja");
    },

    getRezultatiTekmovanja(tekmovanjeId) {
        return this.request(`/tekmovanja/${tekmovanjeId}/rezultati`);
    },

    searchTekmovalci(ime) {
        const params = new URLSearchParams({ ime });
        return this.request(`/tekmovalci/iskanje?${params.toString()}`);
    },

    getNastopiTekmovalca(tekmovalecId) {
        return this.request(`/tekmovalci/${tekmovalecId}/nastopi`);
    },

    getNajboljsiCas(tekmovalecId) {
        return this.request(`/tekmovalci/${tekmovalecId}/najboljsi-cas`);
    },

    primerjajTekmovalca(tekmovalec1Id, tekmovalec2Id) {
        const params = new URLSearchParams({
            tekmovalec1: tekmovalec1Id,
            tekmovalec2: tekmovalec2Id
        });

        return this.request(`/primerjava?${params.toString()}`);
    }
};