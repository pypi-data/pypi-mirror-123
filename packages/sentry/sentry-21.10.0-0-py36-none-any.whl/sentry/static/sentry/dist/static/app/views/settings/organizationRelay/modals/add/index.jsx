Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const list_1 = (0, tslib_1.__importDefault)(require("app/components/list"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const modalManager_1 = (0, tslib_1.__importDefault)(require("../modalManager"));
const item_1 = (0, tslib_1.__importDefault)(require("./item"));
const terminal_1 = (0, tslib_1.__importDefault)(require("./terminal"));
class Add extends modalManager_1.default {
    getTitle() {
        return (0, locale_1.t)('Register Key');
    }
    getBtnSaveLabel() {
        return (0, locale_1.t)('Register');
    }
    getData() {
        const { savedRelays } = this.props;
        const trustedRelays = [...savedRelays, this.state.values];
        return { trustedRelays };
    }
    getContent() {
        return (<StyledList symbol="colored-numeric">
        <item_1.default title={(0, locale_1.tct)('Initialize the configuration. [link: Learn how]', {
                link: (<externalLink_1.default href="https://docs.sentry.io/product/relay/getting-started/#initializing-configuration"/>),
            })} subtitle={(0, locale_1.t)('Within your terminal:')}>
          <terminal_1.default command="relay config init"/>
        </item_1.default>
        <item_1.default title={(0, locale_1.tct)('Go to the file [jsonFile: credentials.json] to find the public key and enter it below.', {
                jsonFile: (<externalLink_1.default href="https://docs.sentry.io/product/relay/getting-started/#registering-relay-with-sentry"/>),
            })}>
          {super.getForm()}
        </item_1.default>
      </StyledList>);
    }
}
exports.default = Add;
const StyledList = (0, styled_1.default)(list_1.default) `
  display: grid;
  grid-gap: ${(0, space_1.default)(3)};
`;
//# sourceMappingURL=index.jsx.map