Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const eventDataSection_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventDataSection"));
const locale_1 = require("app/locale");
const eventDataContent_1 = (0, tslib_1.__importDefault)(require("./eventDataContent"));
const EventExtraData = (0, react_1.memo)(({ event }) => {
    const [raw, setRaw] = (0, react_1.useState)(false);
    return (<eventDataSection_1.default type="extra" title={(0, locale_1.t)('Additional Data')} toggleRaw={() => setRaw(!raw)} raw={raw}>
        <eventDataContent_1.default raw={raw} data={event.context}/>
      </eventDataSection_1.default>);
}, (prevProps, nextProps) => prevProps.event.id !== nextProps.event.id);
exports.default = EventExtraData;
//# sourceMappingURL=eventExtraData.jsx.map