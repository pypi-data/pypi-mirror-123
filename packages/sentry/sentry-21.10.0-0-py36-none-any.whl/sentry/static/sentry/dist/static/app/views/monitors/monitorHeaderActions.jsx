Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const logging_1 = require("app/utils/logging");
const useApi_1 = (0, tslib_1.__importDefault)(require("app/utils/useApi"));
const MonitorHeaderActions = ({ monitor, orgId, onUpdate }) => {
    const api = (0, useApi_1.default)();
    const handleDelete = () => {
        const redirectPath = `/organizations/${orgId}/monitors/`;
        (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Deleting Monitor...'));
        api
            .requestPromise(`/monitors/${monitor.id}/`, {
            method: 'DELETE',
        })
            .then(() => {
            react_router_1.browserHistory.push(redirectPath);
        })
            .catch(() => {
            (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to remove monitor.'));
        });
    };
    const updateMonitor = (data) => {
        (0, indicator_1.addLoadingMessage)();
        api
            .requestPromise(`/monitors/${monitor.id}/`, {
            method: 'PUT',
            data,
        })
            .then(resp => {
            (0, indicator_1.clearIndicators)();
            onUpdate === null || onUpdate === void 0 ? void 0 : onUpdate(resp);
        })
            .catch(err => {
            (0, logging_1.logException)(err);
            (0, indicator_1.addErrorMessage)((0, locale_1.t)('Unable to update monitor.'));
        });
    };
    const toggleStatus = () => updateMonitor({
        status: monitor.status === 'disabled' ? 'active' : 'disabled',
    });
    return (<ButtonContainer>
      <buttonBar_1.default gap={1}>
        <button_1.default size="small" icon={<icons_1.IconEdit size="xs"/>} to={`/organizations/${orgId}/monitors/${monitor.id}/edit/`}>
          &nbsp;
          {(0, locale_1.t)('Edit')}
        </button_1.default>
        <button_1.default size="small" onClick={toggleStatus}>
          {monitor.status !== 'disabled' ? (0, locale_1.t)('Pause') : (0, locale_1.t)('Enable')}
        </button_1.default>
        <confirm_1.default onConfirm={handleDelete} message={(0, locale_1.t)('Deleting this monitor is permanent. Are you sure you wish to continue?')}>
          <button_1.default size="small" icon={<icons_1.IconDelete size="xs"/>}>
            {(0, locale_1.t)('Delete')}
          </button_1.default>
        </confirm_1.default>
      </buttonBar_1.default>
    </ButtonContainer>);
};
const ButtonContainer = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(3)};
  display: flex;
  flex-shrink: 1;
`;
exports.default = MonitorHeaderActions;
//# sourceMappingURL=monitorHeaderActions.jsx.map