Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const integrationIcon_1 = (0, tslib_1.__importDefault)(require("app/views/organizationIntegrations/integrationIcon"));
class IntegrationItem extends react_1.Component {
    render() {
        const { integration, compact } = this.props;
        return (<Flex>
        <div>
          <integrationIcon_1.default size={compact ? 22 : 32} integration={integration}/>
        </div>
        <Labels compact={compact}>
          <IntegrationName data-test-id="integration-name">
            {integration.name}
          </IntegrationName>
          <DomainName compact={compact}>{integration.domainName}</DomainName>
        </Labels>
      </Flex>);
    }
}
exports.default = IntegrationItem;
IntegrationItem.defaultProps = {
    compact: false,
};
const Flex = (0, styled_1.default)('div') `
  display: flex;
`;
const Labels = (0, styled_1.default)('div') `
  box-sizing: border-box;
  display: flex;
  ${p => (p.compact ? 'align-items: center;' : '')};
  flex-direction: ${p => (p.compact ? 'row' : 'column')};
  padding-left: ${(0, space_1.default)(1)};
  min-width: 0;
  justify-content: center;
`;
const IntegrationName = (0, styled_1.default)('div') `
  font-size: 1.6rem;
`;
// Not using the overflowEllipsis style import here
// as it sets width 100% which causes layout issues in the
// integration list.
const DomainName = (0, styled_1.default)('div') `
  color: ${p => (p.compact ? p.theme.gray200 : p.theme.gray400)};
  margin-left: ${p => (p.compact ? (0, space_1.default)(1) : 'inherit')};
  margin-top: ${p => (!p.compact ? (0, space_1.default)(0.25) : 'inherit')};
  font-size: 1.4rem;
  line-height: 1.2;
  overflow: hidden;
  text-overflow: ellipsis;
`;
//# sourceMappingURL=integrationItem.jsx.map