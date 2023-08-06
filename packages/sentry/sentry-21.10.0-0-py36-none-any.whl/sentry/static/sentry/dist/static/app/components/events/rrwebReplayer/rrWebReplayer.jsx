Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const rrweb_player_1 = (0, tslib_1.__importDefault)(require("rrweb-player"));
const BaseRRWebReplayer = ({ url, className }) => {
    const [playerEl, setPlayerEl] = (0, react_1.useState)(null);
    const [events, setEvents] = (0, react_1.useState)();
    const loadEvents = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        try {
            const resp = yield fetch(url);
            const data = yield resp.json();
            setEvents(data.events);
        }
        catch (err) {
            Sentry.captureException(err);
        }
    });
    (0, react_1.useEffect)(() => void loadEvents(), [url]);
    const initPlayer = () => {
        if (events === undefined) {
            return;
        }
        if (playerEl === null) {
            return;
        }
        // eslint-disable-next-line no-new
        new rrweb_player_1.default({
            target: playerEl,
            props: { events, autoPlay: false },
        });
    };
    (0, react_1.useEffect)(() => void initPlayer(), [events, playerEl]);
    return <div ref={el => setPlayerEl(el)} className={className}/>;
};
exports.default = BaseRRWebReplayer;
//# sourceMappingURL=rrWebReplayer.jsx.map