Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const capitalize_1 = (0, tslib_1.__importDefault)(require("lodash/capitalize"));
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const panels_1 = require("app/components/panels");
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const integrationUtil_1 = require("app/utils/integrationUtil");
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
class IntegrationExternalMappings extends react_1.Component {
    render() {
        const { integration, mappings, type, onCreateOrEdit, onDelete } = this.props;
        return (<react_1.Fragment>
        <panels_1.Panel>
          <panels_1.PanelHeader disablePadding hasButtons>
            <HeaderLayout>
              <ExternalNameColumn>{(0, locale_1.tct)('External [type]', { type })}</ExternalNameColumn>
              <SentryNameColumn>{(0, locale_1.tct)('Sentry [type]', { type })}</SentryNameColumn>
              <access_1.default access={['org:integrations']}>
                {({ hasAccess }) => (<ButtonColumn>
                    <tooltip_1.default title={(0, locale_1.tct)('You must be an organization owner, manager or admin to edit or remove a [type] mapping.', { type })} disabled={hasAccess}>
                      <AddButton data-test-id="add-mapping-button" onClick={() => onCreateOrEdit()} size="xsmall" icon={<icons_1.IconAdd size="xs" isCircled/>} disabled={!hasAccess}>
                        {(0, locale_1.tct)('Add [type] Mapping', { type })}
                      </AddButton>
                    </tooltip_1.default>
                  </ButtonColumn>)}
              </access_1.default>
            </HeaderLayout>
          </panels_1.PanelHeader>
          <panels_1.PanelBody>
            {!mappings.length && (<emptyMessage_1.default icon={(0, integrationUtil_1.getIntegrationIcon)(integration.provider.key, 'lg')}>
                {(0, locale_1.tct)('Set up External [type] Mappings.', { type: (0, capitalize_1.default)(type) })}
              </emptyMessage_1.default>)}
            {mappings.map(item => (<access_1.default access={['org:integrations']} key={item.id}>
                {({ hasAccess }) => (<ConfigPanelItem>
                    <Layout>
                      <ExternalNameColumn>{item.externalName}</ExternalNameColumn>
                      <SentryNameColumn>{item.sentryName}</SentryNameColumn>
                      <ButtonColumn>
                        <tooltip_1.default title={(0, locale_1.t)('You must be an organization owner, manager or admin to edit or remove an external user mapping.')} disabled={hasAccess}>
                          <StyledButton size="small" icon={<icons_1.IconEdit size="sm"/>} label={(0, locale_1.t)('edit')} disabled={!hasAccess} onClick={() => onCreateOrEdit(item)}/>
                          <confirm_1.default disabled={!hasAccess} onConfirm={() => onDelete(item)} message={(0, locale_1.t)('Are you sure you want to remove this external user mapping?')}>
                            <StyledButton size="small" icon={<icons_1.IconDelete size="sm"/>} label={(0, locale_1.t)('delete')} disabled={!hasAccess}/>
                          </confirm_1.default>
                        </tooltip_1.default>
                      </ButtonColumn>
                    </Layout>
                  </ConfigPanelItem>)}
              </access_1.default>))}
          </panels_1.PanelBody>
        </panels_1.Panel>
      </react_1.Fragment>);
    }
}
exports.default = IntegrationExternalMappings;
const AddButton = (0, styled_1.default)(button_1.default) `
  text-transform: capitalize;
`;
const Layout = (0, styled_1.default)('div') `
  display: grid;
  grid-column-gap: ${(0, space_1.default)(1)};
  width: 100%;
  align-items: center;
  grid-template-columns: 2.5fr 2.5fr 1fr;
  grid-template-areas: 'external-name sentry-name button';
`;
const HeaderLayout = (0, styled_1.default)(Layout) `
  align-items: center;
  margin: 0;
  margin-left: ${(0, space_1.default)(2)};
  text-transform: uppercase;
`;
const ConfigPanelItem = (0, styled_1.default)(panels_1.PanelItem) ``;
const StyledButton = (0, styled_1.default)(button_1.default) `
  margin: ${(0, space_1.default)(0.5)};
`;
// Columns below
const Column = (0, styled_1.default)('span') `
  overflow: hidden;
  overflow-wrap: break-word;
`;
const ExternalNameColumn = (0, styled_1.default)(Column) `
  grid-area: external-name;
`;
const SentryNameColumn = (0, styled_1.default)(Column) `
  grid-area: sentry-name;
`;
const ButtonColumn = (0, styled_1.default)(Column) `
  grid-area: button;
  text-align: right;
`;
//# sourceMappingURL=integrationExternalMappings.jsx.map