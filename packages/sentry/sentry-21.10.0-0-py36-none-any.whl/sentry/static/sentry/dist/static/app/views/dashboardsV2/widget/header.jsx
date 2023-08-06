Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const breadcrumbs_1 = (0, tslib_1.__importDefault)(require("app/components/breadcrumbs"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const editableText_1 = (0, tslib_1.__importDefault)(require("app/components/editableText"));
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const locale_1 = require("app/locale");
function Header({ title, orgSlug, goBackLocation, dashboardTitle, onChangeTitle, onSave, onDelete, isEditing, }) {
    return (<Layout.Header>
      <Layout.HeaderContent>
        <breadcrumbs_1.default crumbs={[
            {
                to: `/organizations/${orgSlug}/dashboards/`,
                label: (0, locale_1.t)('Dashboards'),
            },
            {
                to: goBackLocation,
                label: dashboardTitle,
            },
            { label: (0, locale_1.t)('Widget Builder') },
        ]}/>
        <Layout.Title>
          <editableText_1.default value={title} onChange={onChangeTitle} errorMessage={(0, locale_1.t)('Please set a title for this widget')} successMessage={(0, locale_1.t)('Widget title updated successfully')}/>
        </Layout.Title>
      </Layout.HeaderContent>

      <Layout.HeaderActions>
        <buttonBar_1.default gap={1}>
          <button_1.default title={(0, locale_1.t)("You’re seeing the metrics project because you have the feature flag 'organizations:metrics' enabled. Send us feedback via email.")} href="mailto:metrics-feedback@sentry.io?subject=Metrics Feedback">
            {(0, locale_1.t)('Give Feedback')}
          </button_1.default>
          <button_1.default to={goBackLocation}>{(0, locale_1.t)('Cancel')}</button_1.default>
          {isEditing && onDelete && (<confirm_1.default priority="danger" message={(0, locale_1.t)('Are you sure you want to delete this widget?')} onConfirm={onDelete}>
              <button_1.default priority="danger">{(0, locale_1.t)('Delete')}</button_1.default>
            </confirm_1.default>)}
          <button_1.default priority="primary" onClick={onSave} disabled={!onSave} title={!onSave ? (0, locale_1.t)('This feature is not yet available') : undefined}>
            {isEditing ? (0, locale_1.t)('Update Widget') : (0, locale_1.t)('Add Widget')}
          </button_1.default>
        </buttonBar_1.default>
      </Layout.HeaderActions>
    </Layout.Header>);
}
exports.default = Header;
//# sourceMappingURL=header.jsx.map