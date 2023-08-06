Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const modal_1 = require("app/actionCreators/modal");
const actionLink_1 = (0, tslib_1.__importDefault)(require("app/components/actions/actionLink"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const customResolutionModal_1 = (0, tslib_1.__importDefault)(require("app/components/customResolutionModal"));
const dropdownLink_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownLink"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const types_1 = require("app/types");
const analytics_1 = require("app/utils/analytics");
const formatters_1 = require("app/utils/formatters");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const button_1 = (0, tslib_1.__importDefault)(require("./button"));
const menuHeader_1 = (0, tslib_1.__importDefault)(require("./menuHeader"));
const menuItemActionLink_1 = (0, tslib_1.__importDefault)(require("./menuItemActionLink"));
const defaultProps = {
    isResolved: false,
    isAutoResolved: false,
    confirmLabel: (0, locale_1.t)('Resolve'),
};
class ResolveActions extends React.Component {
    constructor() {
        super(...arguments);
        this.handleCurrentReleaseResolution = () => {
            const { onUpdate, organization, hasRelease, latestRelease } = this.props;
            hasRelease &&
                onUpdate({
                    status: types_1.ResolutionStatus.RESOLVED,
                    statusDetails: {
                        inRelease: latestRelease ? latestRelease.version : 'latest',
                    },
                });
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'resolve_issue',
                eventName: 'Resolve Issue',
                release: 'current',
                organization_id: organization.id,
            });
        };
        this.handleNextReleaseResolution = () => {
            const { onUpdate, organization, hasRelease } = this.props;
            hasRelease &&
                onUpdate({
                    status: types_1.ResolutionStatus.RESOLVED,
                    statusDetails: {
                        inNextRelease: true,
                    },
                });
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'resolve_issue',
                eventName: 'Resolve Issue',
                release: 'next',
                organization_id: organization.id,
            });
        };
    }
    handleAnotherExistingReleaseResolution(statusDetails) {
        const { organization, onUpdate } = this.props;
        onUpdate({
            status: types_1.ResolutionStatus.RESOLVED,
            statusDetails,
        });
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'resolve_issue',
            eventName: 'Resolve Issue',
            release: 'anotherExisting',
            organization_id: organization.id,
        });
    }
    renderResolved() {
        const { isAutoResolved, onUpdate } = this.props;
        return (<tooltip_1.default title={isAutoResolved
                ? (0, locale_1.t)('This event is resolved due to the Auto Resolve configuration for this project')
                : (0, locale_1.t)('Unresolve')}>
        <button_1.default priority="primary" icon={<icons_1.IconCheckmark size="xs"/>} label={(0, locale_1.t)('Unresolve')} disabled={isAutoResolved} onClick={() => onUpdate({ status: types_1.ResolutionStatus.UNRESOLVED })}/>
      </tooltip_1.default>);
    }
    renderDropdownMenu() {
        const { projectSlug, isResolved, hasRelease, latestRelease, confirmMessage, shouldConfirm, disabled, confirmLabel, disableDropdown, } = this.props;
        if (isResolved) {
            return this.renderResolved();
        }
        const actionTitle = !hasRelease
            ? (0, locale_1.t)('Set up release tracking in order to use this feature.')
            : '';
        const actionLinkProps = {
            shouldConfirm,
            message: confirmMessage,
            confirmLabel,
            disabled: disabled || !hasRelease,
        };
        return (<dropdownLink_1.default customTitle={<button_1.default label={(0, locale_1.t)('More resolve options')} disabled={!projectSlug ? disabled : disableDropdown} icon={<icons_1.IconChevron direction="down" size="xs"/>}/>} caret={false} alwaysRenderMenu disabled={!projectSlug ? disabled : disableDropdown}>
        <menuHeader_1.default>{(0, locale_1.t)('Resolved In')}</menuHeader_1.default>

        <menuItemActionLink_1.default {...actionLinkProps} title={(0, locale_1.t)('The next release')} onAction={this.handleNextReleaseResolution}>
          <tooltip_1.default disabled={hasRelease} title={actionTitle}>
            {(0, locale_1.t)('The next release')}
          </tooltip_1.default>
        </menuItemActionLink_1.default>

        <menuItemActionLink_1.default {...actionLinkProps} title={(0, locale_1.t)('The current release')} onAction={this.handleCurrentReleaseResolution}>
          <tooltip_1.default disabled={hasRelease} title={actionTitle}>
            {latestRelease
                ? (0, locale_1.t)('The current release (%s)', (0, formatters_1.formatVersion)(latestRelease.version))
                : (0, locale_1.t)('The current release')}
          </tooltip_1.default>
        </menuItemActionLink_1.default>

        <menuItemActionLink_1.default {...actionLinkProps} title={(0, locale_1.t)('Another existing release')} onAction={() => hasRelease && this.openCustomReleaseModal()} shouldConfirm={false}>
          <tooltip_1.default disabled={hasRelease} title={actionTitle}>
            {(0, locale_1.t)('Another existing release')}
          </tooltip_1.default>
        </menuItemActionLink_1.default>
      </dropdownLink_1.default>);
    }
    openCustomReleaseModal() {
        const { orgSlug, projectSlug } = this.props;
        (0, modal_1.openModal)(deps => (<customResolutionModal_1.default {...deps} onSelected={(statusDetails) => this.handleAnotherExistingReleaseResolution(statusDetails)} orgSlug={orgSlug} projectSlug={projectSlug}/>));
    }
    render() {
        const { isResolved, onUpdate, confirmMessage, shouldConfirm, disabled, confirmLabel, projectFetchError, } = this.props;
        if (isResolved) {
            return this.renderResolved();
        }
        const actionLinkProps = {
            shouldConfirm,
            message: confirmMessage,
            confirmLabel,
            disabled,
        };
        return (<tooltip_1.default disabled={!projectFetchError} title={(0, locale_1.t)('Error fetching project')}>
        <buttonBar_1.default merged>
          <actionLink_1.default {...actionLinkProps} type="button" title={(0, locale_1.t)('Resolve')} icon={<icons_1.IconCheckmark size="xs"/>} onAction={() => onUpdate({ status: types_1.ResolutionStatus.RESOLVED })}>
            {(0, locale_1.t)('Resolve')}
          </actionLink_1.default>
          {this.renderDropdownMenu()}
        </buttonBar_1.default>
      </tooltip_1.default>);
    }
}
ResolveActions.defaultProps = defaultProps;
exports.default = (0, withOrganization_1.default)(ResolveActions);
//# sourceMappingURL=resolve.jsx.map