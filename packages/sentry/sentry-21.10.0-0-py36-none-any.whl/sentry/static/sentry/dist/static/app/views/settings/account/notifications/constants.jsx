Object.defineProperty(exports, "__esModule", { value: true });
exports.CONFIRMATION_MESSAGE = exports.SELF_NOTIFICATION_SETTINGS_TYPES = exports.NOTIFICATION_SETTINGS_TYPES = exports.MIN_PROJECTS_FOR_PAGINATION = exports.MIN_PROJECTS_FOR_SEARCH = exports.MIN_PROJECTS_FOR_CONFIRMATION = exports.VALUE_MAPPING = exports.ALL_PROVIDERS = void 0;
const locale_1 = require("app/locale");
exports.ALL_PROVIDERS = {
    email: 'default',
    slack: 'never',
};
/**
 * These values are stolen from the DB.
 */
exports.VALUE_MAPPING = {
    default: 0,
    never: 10,
    always: 20,
    subscribe_only: 30,
    committed_only: 40,
};
exports.MIN_PROJECTS_FOR_CONFIRMATION = 3;
exports.MIN_PROJECTS_FOR_SEARCH = 3;
exports.MIN_PROJECTS_FOR_PAGINATION = 100;
exports.NOTIFICATION_SETTINGS_TYPES = [
    'alerts',
    'workflow',
    'deploy',
    'reports',
    'email',
];
exports.SELF_NOTIFICATION_SETTINGS_TYPES = [
    'personalActivityNotifications',
    'selfAssignOnResolve',
];
exports.CONFIRMATION_MESSAGE = (<div>
    <p style={{ marginBottom: '20px' }}>
      <strong>Are you sure you want to disable these notifications?</strong>
    </p>
    <p>
      {(0, locale_1.t)('Turning this off will irreversibly overwrite all of your fine-tuning settings to "off".')}
    </p>
  </div>);
//# sourceMappingURL=constants.jsx.map