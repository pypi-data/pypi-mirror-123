Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const clippedBox_1 = (0, tslib_1.__importDefault)(require("app/components/clippedBox"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const panels_1 = require("app/components/panels");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const recreateRoute_1 = (0, tslib_1.__importDefault)(require("app/utils/recreateRoute"));
const projectKeyCredentials_1 = (0, tslib_1.__importDefault)(require("app/views/settings/project/projectKeys/projectKeyCredentials"));
class KeyRow extends react_1.Component {
    constructor() {
        super(...arguments);
        this.handleRemove = () => {
            const { data, onRemove } = this.props;
            onRemove(data);
        };
        this.handleEnable = () => {
            const { onToggle, data } = this.props;
            onToggle(true, data);
        };
        this.handleDisable = () => {
            const { onToggle, data } = this.props;
            onToggle(false, data);
        };
    }
    render() {
        const { access, data, routes, location, params } = this.props;
        const editUrl = (0, recreateRoute_1.default)(`${data.id}/`, { routes, params, location });
        const controlActive = access.has('project:write');
        const controls = [
            <button_1.default key="edit" to={editUrl} size="small">
        {(0, locale_1.t)('Configure')}
      </button_1.default>,
            <button_1.default key="toggle" size="small" onClick={data.isActive ? this.handleDisable : this.handleEnable} disabled={!controlActive}>
        {data.isActive ? (0, locale_1.t)('Disable') : (0, locale_1.t)('Enable')}
      </button_1.default>,
            <confirm_1.default key="remove" priority="danger" disabled={!controlActive} onConfirm={this.handleRemove} confirmText={(0, locale_1.t)('Remove Key')} message={(0, locale_1.t)('Are you sure you want to remove this key? This action is irreversible.')}>
        <button_1.default size="small" disabled={!controlActive} icon={<icons_1.IconDelete />}/>
      </confirm_1.default>,
        ];
        return (<panels_1.Panel>
        <panels_1.PanelHeader hasButtons>
          <Title disabled={!data.isActive}>
            <PanelHeaderLink to={editUrl}>{data.label}</PanelHeaderLink>
            {!data.isActive && (<small>
                {' \u2014  '}
                {(0, locale_1.t)('Disabled')}
              </small>)}
          </Title>
          <Controls>
            {controls.map((c, n) => (<span key={n}> {c}</span>))}
          </Controls>
        </panels_1.PanelHeader>

        <StyledClippedBox clipHeight={300} defaultClipped btnText={(0, locale_1.t)('Expand')}>
          <StyledPanelBody disabled={!data.isActive}>
            <projectKeyCredentials_1.default projectId={`${data.projectId}`} data={data}/>
          </StyledPanelBody>
        </StyledClippedBox>
      </panels_1.Panel>);
    }
}
exports.default = KeyRow;
const StyledClippedBox = (0, styled_1.default)(clippedBox_1.default) `
  padding: 0;
  margin: 0;
  > *:last-child {
    padding-bottom: ${(0, space_1.default)(3)};
  }
`;
const PanelHeaderLink = (0, styled_1.default)(link_1.default) `
  color: ${p => p.theme.subText};
`;
const Title = (0, styled_1.default)('div') `
  flex: 1;
  ${p => (p.disabled ? 'opacity: 0.5;' : '')};
  margin-right: ${(0, space_1.default)(1)};
`;
const Controls = (0, styled_1.default)('div') `
  display: grid;
  align-items: center;
  grid-gap: ${(0, space_1.default)(1)};
  grid-auto-flow: column;
`;
const StyledPanelBody = (0, styled_1.default)(panels_1.PanelBody) `
  ${p => (p.disabled ? 'opacity: 0.5;' : '')};
`;
//# sourceMappingURL=keyRow.jsx.map