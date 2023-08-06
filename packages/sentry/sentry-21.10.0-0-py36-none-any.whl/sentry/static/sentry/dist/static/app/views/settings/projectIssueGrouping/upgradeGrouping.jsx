Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const indicator_1 = require("app/actionCreators/indicator");
const projectActions_1 = (0, tslib_1.__importDefault)(require("app/actions/projectActions"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const confirm_1 = require("app/components/confirm");
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const handleXhrErrorResponse_1 = (0, tslib_1.__importDefault)(require("app/utils/handleXhrErrorResponse"));
const marked_1 = (0, tslib_1.__importDefault)(require("app/utils/marked"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
const utils_1 = require("./utils");
const upgradeGroupingId = 'upgrade-grouping';
function UpgradeGrouping({ groupingConfigs, organization, projectId, project, onUpgrade, api, location, }) {
    const hasProjectWriteAccess = organization.access.includes('project:write');
    const { updateNotes, riskLevel, latestGroupingConfig } = (0, utils_1.getGroupingChanges)(project, groupingConfigs);
    const { riskNote, alertType } = (0, utils_1.getGroupingRisk)(riskLevel);
    const noUpdates = !latestGroupingConfig;
    const priority = riskLevel >= 2 ? 'danger' : 'primary';
    (0, react_1.useEffect)(() => {
        if (location.hash !== `#${upgradeGroupingId}` ||
            noUpdates ||
            !groupingConfigs ||
            !hasProjectWriteAccess) {
            return;
        }
        handleOpenConfirmModal();
    }, [location.hash]);
    if (!groupingConfigs) {
        return null;
    }
    function handleConfirmUpgrade() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const newData = {};
            if (latestGroupingConfig) {
                const now = Math.floor(new Date().getTime() / 1000);
                const ninety_days = 3600 * 24 * 90;
                newData.groupingConfig = latestGroupingConfig.id;
                newData.secondaryGroupingConfig = project.groupingConfig;
                newData.secondaryGroupingExpiry = now + ninety_days;
            }
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Changing grouping\u2026'));
            try {
                const response = yield api.requestPromise(`/projects/${organization.slug}/${projectId}/`, {
                    method: 'PUT',
                    data: newData,
                });
                (0, indicator_1.clearIndicators)();
                projectActions_1.default.updateSuccess(response);
                onUpgrade();
            }
            catch (_a) {
                (0, handleXhrErrorResponse_1.default)((0, locale_1.t)('Unable to upgrade config'));
            }
        });
    }
    function handleOpenConfirmModal() {
        (0, confirm_1.openConfirmModal)({
            confirmText: (0, locale_1.t)('Upgrade'),
            priority,
            onConfirm: handleConfirmUpgrade,
            message: (<react_1.Fragment>
          <textBlock_1.default>
            <strong>{(0, locale_1.t)('Upgrade Grouping Strategy')}</strong>
          </textBlock_1.default>
          <textBlock_1.default>
            {(0, locale_1.t)('You can upgrade the grouping strategy to the latest but this is an irreversible operation.')}
          </textBlock_1.default>
          <textBlock_1.default>
            <strong>{(0, locale_1.t)('New Behavior')}</strong>
            <div dangerouslySetInnerHTML={{ __html: (0, marked_1.default)(updateNotes) }}/>
          </textBlock_1.default>
          <textBlock_1.default>
            <alert_1.default type={alertType}>{riskNote}</alert_1.default>
          </textBlock_1.default>
        </react_1.Fragment>),
        });
    }
    function getButtonTitle() {
        if (!hasProjectWriteAccess) {
            return (0, locale_1.t)('You do not have sufficient permissions to do this');
        }
        if (noUpdates) {
            return (0, locale_1.t)('You are already on the latest version');
        }
        return undefined;
    }
    return (<panels_1.Panel id={upgradeGroupingId}>
      <panels_1.PanelHeader>{(0, locale_1.t)('Upgrade Grouping')}</panels_1.PanelHeader>
      <panels_1.PanelBody>
        <field_1.default label={(0, locale_1.t)('Upgrade Grouping Strategy')} help={(0, locale_1.tct)('If the project uses an old grouping strategy an update is possible.[linebreak]Doing so will cause new events to group differently.', {
            linebreak: <br />,
        })} disabled>
          <div>
            <button_1.default onClick={handleOpenConfirmModal} disabled={!hasProjectWriteAccess || noUpdates} title={getButtonTitle()} type="button" priority={priority}>
              {(0, locale_1.t)('Upgrade Grouping Strategy')}
            </button_1.default>
          </div>
        </field_1.default>
      </panels_1.PanelBody>
    </panels_1.Panel>);
}
exports.default = UpgradeGrouping;
//# sourceMappingURL=upgradeGrouping.jsx.map