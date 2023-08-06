Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const featureDisabled_1 = (0, tslib_1.__importDefault)(require("app/components/acl/featureDisabled"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const dataExport_1 = (0, tslib_1.__importStar)(require("app/components/dataExport"));
const hovercard_1 = (0, tslib_1.__importDefault)(require("app/components/hovercard"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const analytics_1 = require("app/utils/analytics");
const utils_1 = require("../utils");
function handleDownloadAsCsv(title, { organization, eventView, tableData }) {
    (0, analytics_1.trackAnalyticsEvent)({
        eventKey: 'discover_v2.results.download_csv',
        eventName: 'Discoverv2: Download CSV',
        organization_id: parseInt(organization.id, 10),
    });
    (0, utils_1.downloadAsCsv)(tableData, eventView.getColumns(), title);
}
function renderDownloadButton(canEdit, props) {
    return (<feature_1.default features={['organizations:discover-query']} renderDisabled={() => renderBrowserExportButton(canEdit, props)}>
      {renderAsyncExportButton(canEdit, props)}
    </feature_1.default>);
}
function renderBrowserExportButton(canEdit, props) {
    const { isLoading, error } = props;
    const disabled = isLoading || error !== null || canEdit === false;
    const onClick = disabled ? undefined : () => handleDownloadAsCsv(props.title, props);
    return (<button_1.default size="small" disabled={disabled} onClick={onClick} data-test-id="grid-download-csv" icon={<icons_1.IconDownload size="xs"/>}>
      {(0, locale_1.t)('Export')}
    </button_1.default>);
}
function renderAsyncExportButton(canEdit, props) {
    const { isLoading, error, location, eventView } = props;
    const disabled = isLoading || error !== null || canEdit === false;
    return (<dataExport_1.default payload={{
            queryType: dataExport_1.ExportQueryType.Discover,
            queryInfo: eventView.getEventsAPIPayload(location),
        }} disabled={disabled} icon={<icons_1.IconDownload size="xs"/>}>
      {(0, locale_1.t)('Export All')}
    </dataExport_1.default>);
}
// Placate eslint proptype checking
function renderEditButton(canEdit, props) {
    const onClick = canEdit ? props.onEdit : undefined;
    return (<guideAnchor_1.default target="columns_header_button">
      <button_1.default size="small" disabled={!canEdit} onClick={onClick} data-test-id="grid-edit-enable" icon={<icons_1.IconStack size="xs"/>}>
        {(0, locale_1.t)('Columns')}
      </button_1.default>
    </guideAnchor_1.default>);
}
// Placate eslint proptype checking
function renderSummaryButton({ onChangeShowTags, showTags }) {
    return (<button_1.default size="small" onClick={onChangeShowTags} icon={<icons_1.IconTag size="xs"/>}>
      {showTags ? (0, locale_1.t)('Hide Tags') : (0, locale_1.t)('Show Tags')}
    </button_1.default>);
}
function FeatureWrapper(props) {
    const noEditMessage = (0, locale_1.t)('Requires discover query feature.');
    const editFeatures = ['organizations:discover-query'];
    const renderDisabled = p => (<hovercard_1.default body={<featureDisabled_1.default features={p.features} hideHelpToggle message={noEditMessage} featureName={noEditMessage}/>}>
      {p.children(p)}
    </hovercard_1.default>);
    return (<feature_1.default hookName="feature-disabled:grid-editable-actions" renderDisabled={renderDisabled} features={editFeatures}>
      {({ hasFeature }) => props.children(hasFeature, props)}
    </feature_1.default>);
}
function HeaderActions(props) {
    return (<React.Fragment>
      <FeatureWrapper {...props} key="edit">
        {renderEditButton}
      </FeatureWrapper>
      <FeatureWrapper {...props} key="download">
        {renderDownloadButton}
      </FeatureWrapper>
      {renderSummaryButton(props)}
    </React.Fragment>);
}
exports.default = HeaderActions;
//# sourceMappingURL=tableActions.jsx.map