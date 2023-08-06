Object.defineProperty(exports, "__esModule", { value: true });
exports.CreateAlertFromViewButton = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const navigation_1 = require("app/actionCreators/navigation");
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const fields_1 = require("app/utils/discover/fields");
const useApi_1 = (0, tslib_1.__importDefault)(require("app/utils/useApi"));
const constants_1 = require("app/views/alerts/incidentRules/constants");
const utils_1 = require("app/views/alerts/utils");
/**
 * Displays messages to the user on what needs to change in their query
 */
function IncompatibleQueryAlert({ incompatibleQuery, eventView, orgId, onClose, }) {
    const { hasProjectError, hasEnvironmentError, hasEventTypeError, hasYAxisError } = incompatibleQuery;
    const totalErrors = Object.values(incompatibleQuery).filter(val => val === true).length;
    const eventTypeError = eventView.clone();
    eventTypeError.query += ' event.type:error';
    const eventTypeTransaction = eventView.clone();
    eventTypeTransaction.query += ' event.type:transaction';
    const eventTypeDefault = eventView.clone();
    eventTypeDefault.query += ' event.type:default';
    const eventTypeErrorDefault = eventView.clone();
    eventTypeErrorDefault.query += ' event.type:error or event.type:default';
    const pathname = `/organizations/${orgId}/discover/results/`;
    const eventTypeLinks = {
        error: (<link_1.default to={{
                pathname,
                query: eventTypeError.generateQueryStringObject(),
            }}/>),
        default: (<link_1.default to={{
                pathname,
                query: eventTypeDefault.generateQueryStringObject(),
            }}/>),
        transaction: (<link_1.default to={{
                pathname,
                query: eventTypeTransaction.generateQueryStringObject(),
            }}/>),
        errorDefault: (<link_1.default to={{
                pathname,
                query: eventTypeErrorDefault.generateQueryStringObject(),
            }}/>),
    };
    return (<StyledAlert type="warning" icon={<icons_1.IconInfo color="yellow300" size="sm"/>}>
      {totalErrors === 1 && (<React.Fragment>
          {hasProjectError &&
                (0, locale_1.t)('An alert can use data from only one Project. Select one and try again.')}
          {hasEnvironmentError &&
                (0, locale_1.t)('An alert supports data from a single Environment or All Environments. Pick one try again.')}
          {hasEventTypeError &&
                (0, locale_1.tct)('An alert needs a filter of [error:event.type:error], [default:event.type:default], [transaction:event.type:transaction], [errorDefault:(event.type:error OR event.type:default)]. Use one of these and try again.', eventTypeLinks)}
          {hasYAxisError &&
                (0, locale_1.tct)('An alert can’t use the metric [yAxis] just yet. Select another metric and try again.', {
                    yAxis: <StyledCode>{eventView.getYAxis()}</StyledCode>,
                })}
        </React.Fragment>)}
      {totalErrors > 1 && (<React.Fragment>
          {(0, locale_1.t)('Yikes! That button didn’t work. Please fix the following problems:')}
          <StyledUnorderedList>
            {hasProjectError && <li>{(0, locale_1.t)('Select one Project.')}</li>}
            {hasEnvironmentError && (<li>{(0, locale_1.t)('Select a single Environment or All Environments.')}</li>)}
            {hasEventTypeError && (<li>
                {(0, locale_1.tct)('Use the filter [error:event.type:error], [default:event.type:default], [transaction:event.type:transaction], [errorDefault:(event.type:error OR event.type:default)].', eventTypeLinks)}
              </li>)}
            {hasYAxisError && (<li>
                {(0, locale_1.tct)('An alert can’t use the metric [yAxis] just yet. Select another metric and try again.', {
                    yAxis: <StyledCode>{eventView.getYAxis()}</StyledCode>,
                })}
              </li>)}
          </StyledUnorderedList>
        </React.Fragment>)}
      <StyledCloseButton icon={<icons_1.IconClose color="yellow300" size="sm" isCircled/>} aria-label={(0, locale_1.t)('Close')} size="zero" onClick={onClose} borderless/>
    </StyledAlert>);
}
function incompatibleYAxis(eventView) {
    var _a;
    const column = (0, fields_1.explodeFieldString)(eventView.getYAxis());
    if (column.kind === 'field' || column.kind === 'equation') {
        return true;
    }
    const eventTypeMatch = eventView.query.match(/event\.type:(transaction|error)/);
    if (!eventTypeMatch) {
        return false;
    }
    const dataset = eventTypeMatch[1];
    const yAxisConfig = dataset === 'error' ? constants_1.errorFieldConfig : constants_1.transactionFieldConfig;
    const invalidFunction = !yAxisConfig.aggregations.includes(column.function[0]);
    // Allow empty parameters, allow all numeric parameters - eg. apdex(300)
    const aggregation = fields_1.AGGREGATIONS[column.function[0]];
    if (!aggregation) {
        return false;
    }
    const isNumericParameter = aggregation.parameters.some(param => param.kind === 'value' && param.dataType === 'number');
    // There are other measurements possible, but for the time being, only allow alerting
    // on the predefined set of measurements for alerts.
    const allowedParameters = [
        '',
        ...yAxisConfig.fields,
        ...((_a = yAxisConfig.measurementKeys) !== null && _a !== void 0 ? _a : []),
    ];
    const invalidParameter = !isNumericParameter && !allowedParameters.includes(column.function[1]);
    return invalidFunction || invalidParameter;
}
/**
 * Provide a button that can create an alert from an event view.
 * Emits incompatible query issues on click
 */
function CreateAlertFromViewButton(_a) {
    var { projects, eventView, organization, referrer, onIncompatibleQuery, onSuccess } = _a, buttonProps = (0, tslib_1.__rest)(_a, ["projects", "eventView", "organization", "referrer", "onIncompatibleQuery", "onSuccess"]);
    // Must have exactly one project selected and not -1 (all projects)
    const hasProjectError = eventView.project.length !== 1 || eventView.project[0] === -1;
    // Must have one or zero environments
    const hasEnvironmentError = eventView.environment.length > 1;
    // Must have event.type of error or transaction
    const hasEventTypeError = (0, utils_1.getQueryDatasource)(eventView.query) === null;
    // yAxis must be a function and enabled on alerts
    const hasYAxisError = incompatibleYAxis(eventView);
    const errors = {
        hasProjectError,
        hasEnvironmentError,
        hasEventTypeError,
        hasYAxisError,
    };
    const project = projects.find(p => p.id === `${eventView.project[0]}`);
    const hasErrors = Object.values(errors).some(x => x);
    const to = hasErrors
        ? undefined
        : {
            pathname: `/organizations/${organization.slug}/alerts/${project === null || project === void 0 ? void 0 : project.slug}/new/`,
            query: Object.assign(Object.assign({}, eventView.generateQueryStringObject()), { createFromDiscover: true, referrer }),
        };
    const handleClick = (event) => {
        if (hasErrors) {
            event.preventDefault();
            onIncompatibleQuery((onAlertClose) => (<IncompatibleQueryAlert incompatibleQuery={errors} eventView={eventView} orgId={organization.slug} onClose={onAlertClose}/>), errors);
            return;
        }
        onSuccess();
    };
    return (<CreateAlertButton organization={organization} onClick={handleClick} to={to} {...buttonProps}/>);
}
exports.CreateAlertFromViewButton = CreateAlertFromViewButton;
const CreateAlertButton = (0, react_router_1.withRouter)((_a) => {
    var { organization, projectSlug, iconProps, referrer, router, hideIcon, showPermissionGuide } = _a, buttonProps = (0, tslib_1.__rest)(_a, ["organization", "projectSlug", "iconProps", "referrer", "router", "hideIcon", "showPermissionGuide"]);
    const api = (0, useApi_1.default)();
    const createAlertUrl = (providedProj) => {
        const alertsBaseUrl = `/organizations/${organization.slug}/alerts/${providedProj}`;
        return `${alertsBaseUrl}/wizard/${referrer ? `?referrer=${referrer}` : ''}`;
    };
    function handleClickWithoutProject(event) {
        event.preventDefault();
        (0, navigation_1.navigateTo)(createAlertUrl(':projectId'), router);
    }
    function enableAlertsMemberWrite() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const settingsEndpoint = `/organizations/${organization.slug}/`;
            (0, indicator_1.addLoadingMessage)();
            try {
                yield api.requestPromise(settingsEndpoint, {
                    method: 'PUT',
                    data: {
                        alertsMemberWrite: true,
                    },
                });
                (0, indicator_1.addSuccessMessage)((0, locale_1.t)('Successfully updated organization settings'));
            }
            catch (err) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to update organization settings'));
            }
        });
    }
    const permissionTooltipText = (0, locale_1.tct)('Ask your organization owner or manager to [settingsLink:enable alerts access] for you.', { settingsLink: <link_1.default to={`/settings/${organization.slug}`}/> });
    const renderButton = (hasAccess) => {
        var _a;
        return (<button_1.default disabled={!hasAccess} title={!hasAccess ? permissionTooltipText : undefined} icon={!hideIcon && <icons_1.IconSiren {...iconProps}/>} to={projectSlug ? createAlertUrl(projectSlug) : undefined} tooltipProps={{
                isHoverable: true,
                position: 'top',
                popperStyle: {
                    maxWidth: '270px',
                },
            }} onClick={projectSlug ? undefined : handleClickWithoutProject} {...buttonProps}>
        {(_a = buttonProps.children) !== null && _a !== void 0 ? _a : (0, locale_1.t)('Create Alert')}
      </button_1.default>);
    };
    const showGuide = !organization.alertsMemberWrite && !!showPermissionGuide;
    return (<access_1.default organization={organization} access={['alerts:write']}>
        {({ hasAccess }) => showGuide ? (<access_1.default organization={organization} access={['org:write']}>
              {({ hasAccess: isOrgAdmin }) => (<guideAnchor_1.default target={isOrgAdmin ? 'alerts_write_owner' : 'alerts_write_member'} onFinish={isOrgAdmin ? enableAlertsMemberWrite : undefined}>
                  {renderButton(hasAccess)}
                </guideAnchor_1.default>)}
            </access_1.default>) : (renderButton(hasAccess))}
      </access_1.default>);
});
exports.default = CreateAlertButton;
const StyledAlert = (0, styled_1.default)(alert_1.default) `
  color: ${p => p.theme.textColor};
  margin-bottom: 0;
`;
const StyledUnorderedList = (0, styled_1.default)('ul') `
  margin-bottom: 0;
`;
const StyledCode = (0, styled_1.default)('code') `
  background-color: transparent;
  padding: 0;
`;
const StyledCloseButton = (0, styled_1.default)(button_1.default) `
  transition: opacity 0.1s linear;
  position: absolute;
  top: 3px;
  right: 0;

  &:hover,
  &:focus {
    background-color: transparent;
    opacity: 1;
  }
`;
//# sourceMappingURL=createAlertButton.jsx.map