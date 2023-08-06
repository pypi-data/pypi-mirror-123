Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const featureDisabled_1 = (0, tslib_1.__importDefault)(require("app/components/acl/featureDisabled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const hovercard_1 = (0, tslib_1.__importDefault)(require("app/components/hovercard"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const types_1 = require("./types");
class Controls extends React.Component {
    render() {
        const { dashboardState, dashboards, onEdit, onCancel, onCommit, onDelete } = this.props;
        const cancelButton = (<button_1.default data-test-id="dashboard-cancel" onClick={e => {
                e.preventDefault();
                onCancel();
            }}>
        {(0, locale_1.t)('Cancel')}
      </button_1.default>);
        if ([types_1.DashboardState.EDIT, types_1.DashboardState.PENDING_DELETE].includes(dashboardState)) {
            return (<StyledButtonBar gap={1} key="edit-controls">
          {cancelButton}
          <confirm_1.default priority="danger" message={(0, locale_1.t)('Are you sure you want to delete this dashboard?')} onConfirm={onDelete} disabled={dashboards.length <= 1}>
            <button_1.default data-test-id="dashboard-delete" priority="danger">
              {(0, locale_1.t)('Delete')}
            </button_1.default>
          </confirm_1.default>
          <button_1.default data-test-id="dashboard-commit" onClick={e => {
                    e.preventDefault();
                    onCommit();
                }} priority="primary">
            {(0, locale_1.t)('Save and Finish')}
          </button_1.default>
        </StyledButtonBar>);
        }
        if (dashboardState === 'create') {
            return (<StyledButtonBar gap={1} key="create-controls">
          {cancelButton}
          <button_1.default data-test-id="dashboard-commit" onClick={e => {
                    e.preventDefault();
                    onCommit();
                }} priority="primary">
            {(0, locale_1.t)('Save and Finish')}
          </button_1.default>
        </StyledButtonBar>);
        }
        return (<StyledButtonBar gap={1} key="controls">
        <DashboardEditFeature>
          {hasFeature => (<button_1.default data-test-id="dashboard-edit" onClick={e => {
                    e.preventDefault();
                    onEdit();
                }} priority="primary" icon={<icons_1.IconEdit size="xs"/>} disabled={!hasFeature}>
              {(0, locale_1.t)('Edit Dashboard')}
            </button_1.default>)}
        </DashboardEditFeature>
      </StyledButtonBar>);
    }
}
const DashboardEditFeature = ({ children, }) => {
    const noFeatureMessage = (0, locale_1.t)('Requires dashboard editing.');
    const renderDisabled = p => (<hovercard_1.default body={<featureDisabled_1.default features={p.features} hideHelpToggle message={noFeatureMessage} featureName={noFeatureMessage}/>}>
      {p.children(p)}
    </hovercard_1.default>);
    return (<feature_1.default hookName="feature-disabled:dashboards-edit" features={['organizations:dashboards-edit']} renderDisabled={renderDisabled}>
      {({ hasFeature }) => children(hasFeature)}
    </feature_1.default>);
};
const StyledButtonBar = (0, styled_1.default)(buttonBar_1.default) `
  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    grid-auto-flow: row;
    grid-row-gap: ${(0, space_1.default)(1)};
    width: 100%;
  }
`;
exports.default = Controls;
//# sourceMappingURL=controls.jsx.map