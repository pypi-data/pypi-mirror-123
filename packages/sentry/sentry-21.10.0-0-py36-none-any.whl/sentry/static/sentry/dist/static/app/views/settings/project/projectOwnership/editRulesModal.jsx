Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const locale_1 = require("app/locale");
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
const ownerInput_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/projectOwnership/ownerInput"));
class EditOwnershipRulesModal extends react_1.Component {
    render() {
        const { ownership } = this.props;
        return (<react_1.Fragment>
        <Block>
          {(0, locale_1.t)('Rules follow the pattern: ')} <code>type:glob owner owner</code>
        </Block>
        <Block>
          {(0, locale_1.t)('Owners can be team identifiers starting with #, or user emails')}
        </Block>
        <Block>
          {(0, locale_1.t)('Globbing Syntax:')}
          <CodeBlock>{'* matches everything\n? matches any single character'}</CodeBlock>
        </Block>
        <Block>
          {(0, locale_1.t)('Examples')}
          <CodeBlock>
            path:src/example/pipeline/* person@sentry.io #infrastructure
            {'\n'}
            url:http://example.com/settings/* #product
            {'\n'}
            tags.sku_class:enterprise #enterprise
          </CodeBlock>
        </Block>
        {ownership && <ownerInput_1.default {...this.props} initialText={ownership.raw || ''}/>}
      </react_1.Fragment>);
    }
}
const Block = (0, styled_1.default)(textBlock_1.default) `
  margin-bottom: 16px;
`;
const CodeBlock = (0, styled_1.default)('pre') `
  word-break: break-all;
  white-space: pre-wrap;
`;
exports.default = EditOwnershipRulesModal;
//# sourceMappingURL=editRulesModal.jsx.map