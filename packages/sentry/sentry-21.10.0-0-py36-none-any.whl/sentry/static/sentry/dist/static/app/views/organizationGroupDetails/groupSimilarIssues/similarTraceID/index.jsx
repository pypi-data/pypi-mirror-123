Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const body_1 = (0, tslib_1.__importDefault)(require("./body"));
const header_1 = (0, tslib_1.__importDefault)(require("./header"));
const SimilarTraceID = (_a) => {
    var _b, _c;
    var { event } = _a, props = (0, tslib_1.__rest)(_a, ["event"]);
    const traceID = (_c = (_b = event.contexts) === null || _b === void 0 ? void 0 : _b.trace) === null || _c === void 0 ? void 0 : _c.trace_id;
    return (<Wrapper>
      <header_1.default traceID={traceID}/>
      <body_1.default traceID={traceID} event={event} {...props}/>
    </Wrapper>);
};
exports.default = SimilarTraceID;
const Wrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(2)};
`;
//# sourceMappingURL=index.jsx.map