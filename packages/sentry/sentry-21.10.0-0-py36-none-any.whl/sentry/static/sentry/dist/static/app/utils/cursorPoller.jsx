Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const api_1 = require("app/api");
const parseLinkHeader_1 = (0, tslib_1.__importDefault)(require("app/utils/parseLinkHeader"));
const BASE_DELAY = 3000;
const MAX_DELAY = 60000;
class CursorPoller {
    constructor(options) {
        this.api = new api_1.Client();
        this.timeoutId = null;
        this.lastRequest = null;
        this.active = true;
        this.reqsWithoutData = 0;
        this.options = options;
        this.pollingEndpoint = options.endpoint;
    }
    getDelay() {
        const delay = BASE_DELAY * (this.reqsWithoutData + 1);
        return Math.min(delay, MAX_DELAY);
    }
    setEndpoint(url) {
        this.pollingEndpoint = url;
    }
    enable() {
        this.active = true;
        if (!this.timeoutId) {
            this.timeoutId = window.setTimeout(this.poll.bind(this), this.getDelay());
        }
    }
    disable() {
        this.active = false;
        if (this.timeoutId) {
            window.clearTimeout(this.timeoutId);
            this.timeoutId = null;
        }
        if (this.lastRequest) {
            this.lastRequest.cancel();
        }
    }
    poll() {
        this.lastRequest = this.api.request(this.pollingEndpoint, {
            success: (data, _, resp) => {
                var _a;
                // cancel in progress operation if disabled
                if (!this.active) {
                    return;
                }
                // if theres no data, nothing changes
                if (!data || !data.length) {
                    this.reqsWithoutData += 1;
                    return;
                }
                if (this.reqsWithoutData > 0) {
                    this.reqsWithoutData -= 1;
                }
                const linksHeader = (_a = resp === null || resp === void 0 ? void 0 : resp.getResponseHeader('Link')) !== null && _a !== void 0 ? _a : null;
                const links = (0, parseLinkHeader_1.default)(linksHeader);
                this.pollingEndpoint = links.previous.href;
                this.options.success(data, linksHeader);
            },
            error: resp => {
                if (!resp) {
                    return;
                }
                // If user does not have access to the endpoint, we should halt polling
                // These errors could mean:
                // * the user lost access to a project
                // * project was renamed
                // * user needs to reauth
                if (resp.status === 404 || resp.status === 403 || resp.status === 401) {
                    this.disable();
                }
            },
            complete: () => {
                this.lastRequest = null;
                if (this.active) {
                    this.timeoutId = window.setTimeout(this.poll.bind(this), this.getDelay());
                }
            },
        });
    }
}
exports.default = CursorPoller;
//# sourceMappingURL=cursorPoller.jsx.map