Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const emptyStateWarning_1 = (0, tslib_1.__importDefault)(require("app/components/emptyStateWarning"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const panels_1 = require("app/components/panels");
const queryCount_1 = (0, tslib_1.__importDefault)(require("app/components/queryCount"));
const locale_1 = require("app/locale");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const mergedItem_1 = (0, tslib_1.__importDefault)(require("./mergedItem"));
const mergedToolbar_1 = (0, tslib_1.__importDefault)(require("./mergedToolbar"));
function MergedList({ fingerprints = [], pageLinks, onToggleCollapse, onUnmerge, organization, groupId, project, }) {
    const fingerprintsWithLatestEvent = fingerprints.filter(({ latestEvent }) => !!latestEvent);
    const hasResults = fingerprintsWithLatestEvent.length > 0;
    if (!hasResults) {
        return (<panels_1.Panel>
        <emptyStateWarning_1.default>
          <p>{(0, locale_1.t)("There don't seem to be any hashes for this issue.")}</p>
        </emptyStateWarning_1.default>
      </panels_1.Panel>);
    }
    return (<react_1.Fragment>
      <h2>
        <span>{(0, locale_1.t)('Merged fingerprints with latest event')}</span>{' '}
        <queryCount_1.default count={fingerprintsWithLatestEvent.length}/>
      </h2>

      <panels_1.Panel>
        <mergedToolbar_1.default onToggleCollapse={onToggleCollapse} onUnmerge={onUnmerge} orgId={organization.slug} project={project} groupId={groupId}/>

        <panels_1.PanelBody>
          {fingerprintsWithLatestEvent.map(fingerprint => (<mergedItem_1.default key={fingerprint.id} organization={organization} fingerprint={fingerprint}/>))}
        </panels_1.PanelBody>
      </panels_1.Panel>
      {pageLinks && <pagination_1.default pageLinks={pageLinks}/>}
    </react_1.Fragment>);
}
exports.default = (0, withOrganization_1.default)(MergedList);
//# sourceMappingURL=mergedList.jsx.map