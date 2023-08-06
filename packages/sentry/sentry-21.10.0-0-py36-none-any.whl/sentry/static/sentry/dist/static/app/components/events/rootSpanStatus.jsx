Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const styles_1 = require("app/components/charts/styles");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
class RootSpanStatus extends react_1.Component {
    getTransactionEvent() {
        const { event } = this.props;
        if (event.type === 'transaction') {
            return event;
        }
        return undefined;
    }
    getRootSpanStatus() {
        var _a, _b;
        const event = this.getTransactionEvent();
        const DEFAULT = '\u2014';
        if (!event) {
            return DEFAULT;
        }
        const traceContext = (_a = event === null || event === void 0 ? void 0 : event.contexts) === null || _a === void 0 ? void 0 : _a.trace;
        return (_b = traceContext === null || traceContext === void 0 ? void 0 : traceContext.status) !== null && _b !== void 0 ? _b : DEFAULT;
    }
    getHttpStatusCode() {
        const { event } = this.props;
        const { tags } = event;
        if (!Array.isArray(tags)) {
            return '';
        }
        const tag = tags.find(tagObject => tagObject.key === 'http.status_code');
        if (!tag) {
            return '';
        }
        return tag.value;
    }
    render() {
        const event = this.getTransactionEvent();
        if (!event) {
            return null;
        }
        const label = `${this.getHttpStatusCode()} ${this.getRootSpanStatus()}`.trim();
        return (<Container>
        <Header>
          <styles_1.SectionHeading>{(0, locale_1.t)('Status')}</styles_1.SectionHeading>
        </Header>
        <div>{label}</div>
      </Container>);
    }
}
const Container = (0, styled_1.default)('div') `
  color: ${p => p.theme.subText};
  font-size: ${p => p.theme.fontSizeMedium};
  margin-bottom: ${(0, space_1.default)(4)};
`;
const Header = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
`;
exports.default = RootSpanStatus;
//# sourceMappingURL=rootSpanStatus.jsx.map