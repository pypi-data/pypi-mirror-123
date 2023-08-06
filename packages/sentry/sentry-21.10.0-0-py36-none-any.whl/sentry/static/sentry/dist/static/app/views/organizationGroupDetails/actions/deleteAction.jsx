Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const modal_1 = require("app/actionCreators/modal");
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const featureDisabled_1 = (0, tslib_1.__importDefault)(require("app/components/acl/featureDisabled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/actions/button"));
const menuHeader_1 = (0, tslib_1.__importDefault)(require("app/components/actions/menuHeader"));
const menuItemActionLink_1 = (0, tslib_1.__importDefault)(require("app/components/actions/menuItemActionLink"));
const button_2 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const dropdownLink_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownLink"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
function DeleteAction({ disabled, project, organization, onDiscard, onDelete }) {
    function renderDiscardDisabled(_a) {
        var { children } = _a, props = (0, tslib_1.__rest)(_a, ["children"]);
        return children(Object.assign(Object.assign({}, props), { renderDisabled: ({ features }) => (<featureDisabled_1.default alert featureName="Discard and Delete" features={features}/>) }));
    }
    function renderDiscardModal({ Body, Footer, closeModal }) {
        return (<feature_1.default features={['projects:discard-groups']} hookName="feature-disabled:discard-groups" organization={organization} project={project} renderDisabled={renderDiscardDisabled}>
        {(_a) => {
                var { hasFeature, renderDisabled } = _a, props = (0, tslib_1.__rest)(_a, ["hasFeature", "renderDisabled"]);
                return (<react_1.Fragment>
            <Body>
              {!hasFeature &&
                        typeof renderDisabled === 'function' &&
                        renderDisabled(Object.assign(Object.assign({}, props), { hasFeature, children: null }))}
              {(0, locale_1.t)(`Discarding this event will result in the deletion of most data associated with this issue and future events being discarded before reaching your stream. Are you sure you wish to continue?`)}
            </Body>
            <Footer>
              <button_2.default onClick={closeModal}>{(0, locale_1.t)('Cancel')}</button_2.default>
              <button_2.default style={{ marginLeft: (0, space_1.default)(1) }} priority="primary" onClick={onDiscard} disabled={!hasFeature}>
                {(0, locale_1.t)('Discard Future Events')}
              </button_2.default>
            </Footer>
          </react_1.Fragment>);
            }}
      </feature_1.default>);
    }
    function openDiscardModal() {
        (0, modal_1.openModal)(renderDiscardModal);
        (0, analytics_1.analytics)('feature.discard_group.modal_opened', {
            org_id: parseInt(organization.id, 10),
        });
    }
    return (<buttonBar_1.default merged>
      <confirm_1.default message={(0, locale_1.t)('Deleting this issue is permanent. Are you sure you wish to continue?')} onConfirm={onDelete} disabled={disabled}>
        <DeleteButton disabled={disabled} label={(0, locale_1.t)('Delete issue')} icon={<icons_1.IconDelete size="xs"/>}/>
      </confirm_1.default>
      <dropdownLink_1.default caret={false} disabled={disabled} customTitle={<button_1.default disabled={disabled} label={(0, locale_1.t)('More delete options')} icon={<icons_1.IconChevron direction="down" size="xs"/>}/>}>
        <menuHeader_1.default>{(0, locale_1.t)('Delete & Discard')}</menuHeader_1.default>
        <menuItemActionLink_1.default title="" onAction={openDiscardModal}>
          {(0, locale_1.t)('Delete and discard future events')}
        </menuItemActionLink_1.default>
      </dropdownLink_1.default>
    </buttonBar_1.default>);
}
const DeleteButton = (0, styled_1.default)(button_1.default) `
  ${p => !p.disabled &&
    `
  &:hover {
    background-color: ${p.theme.button.danger.background};
    color: ${p.theme.button.danger.color};
    border-color: ${p.theme.button.danger.border};
  }
  `}
`;
exports.default = DeleteAction;
//# sourceMappingURL=deleteAction.jsx.map