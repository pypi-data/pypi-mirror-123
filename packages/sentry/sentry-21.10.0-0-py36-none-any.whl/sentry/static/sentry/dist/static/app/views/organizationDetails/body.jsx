Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const alertActions_1 = (0, tslib_1.__importDefault)(require("app/actions/alertActions"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const footer_1 = (0, tslib_1.__importDefault)(require("app/components/footer"));
const thirds_1 = require("app/components/layouts/thirds");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const useApi_1 = (0, tslib_1.__importDefault)(require("app/utils/useApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
function DeletionInProgress({ organization }) {
    return (<thirds_1.Body>
      <thirds_1.Main>
        <alert_1.default type="warning" icon={<icons_1.IconWarning />}>
          {(0, locale_1.tct)('The [organization] organization is currently in the process of being deleted from Sentry.', {
            organization: <strong>{organization.slug}</strong>,
        })}
        </alert_1.default>
      </thirds_1.Main>
    </thirds_1.Body>);
}
function DeletionPending({ organization }) {
    const api = (0, useApi_1.default)();
    const [isRestoring, setIsRestoring] = (0, react_1.useState)(false);
    const onRestore = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        setIsRestoring(true);
        try {
            yield api.requestPromise(`/organizations/${organization.slug}/`, {
                method: 'PUT',
                data: { cancelDeletion: true },
            });
            window.location.reload();
        }
        catch (_a) {
            setIsRestoring(false);
            alertActions_1.default.addAlert({
                message: 'We were unable to restore this organization. Please try again or contact support.',
                type: 'error',
            });
        }
    });
    return (<thirds_1.Body>
      <thirds_1.Main>
        <h3>{(0, locale_1.t)('Deletion Scheduled')}</h3>
        <p>
          {(0, locale_1.tct)('The [organization] organization is currently scheduled for deletion.', {
            organization: <strong>{organization.slug}</strong>,
        })}
        </p>

        {organization.access.includes('org:admin') ? (<div>
            <p>
              {(0, locale_1.t)('Would you like to cancel this process and restore the organization back to the original state?')}
            </p>
            <p>
              <button_1.default priority="primary" onClick={onRestore} disabled={isRestoring}>
                {(0, locale_1.t)('Restore Organization')}
              </button_1.default>
            </p>
          </div>) : (<p>
            {(0, locale_1.t)('If this is a mistake, contact an organization owner and ask them to restore this organization.')}
          </p>)}
        <p>
          <small>
            {(0, locale_1.t)("Note: Restoration is available until the process begins. Once it does, there's no recovering the data that has been removed.")}
          </small>
        </p>
      </thirds_1.Main>
    </thirds_1.Body>);
}
function OrganizationDetailsBody({ children, organization }) {
    var _a;
    const status = (_a = organization === null || organization === void 0 ? void 0 : organization.status) === null || _a === void 0 ? void 0 : _a.id;
    if (status === 'pending_deletion') {
        return <DeletionPending organization={organization}/>;
    }
    if (status === 'deletion_in_progress') {
        return <DeletionInProgress organization={organization}/>;
    }
    return (<react_1.Fragment>
      <errorBoundary_1.default>{children}</errorBoundary_1.default>
      <footer_1.default />
    </react_1.Fragment>);
}
exports.default = (0, withOrganization_1.default)(OrganizationDetailsBody);
//# sourceMappingURL=body.jsx.map