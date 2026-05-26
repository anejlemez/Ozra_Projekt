const isBackendOrigin = window.location.port === "5000";

const CONFIG = {
    API_BASE_URL: isBackendOrigin ? "" : "http://127.0.0.1:5000",
    MAX_RESULTS_DISPLAY: 500
};