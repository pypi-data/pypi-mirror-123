Object.defineProperty(exports, "__esModule", { value: true });
exports.AlertRuleStatus = exports.IncidentStatusMethod = exports.IncidentStatus = exports.IncidentActivityType = void 0;
var IncidentActivityType;
(function (IncidentActivityType) {
    IncidentActivityType[IncidentActivityType["CREATED"] = 0] = "CREATED";
    IncidentActivityType[IncidentActivityType["DETECTED"] = 1] = "DETECTED";
    IncidentActivityType[IncidentActivityType["STATUS_CHANGE"] = 2] = "STATUS_CHANGE";
    IncidentActivityType[IncidentActivityType["COMMENT"] = 3] = "COMMENT";
    IncidentActivityType[IncidentActivityType["STARTED"] = 4] = "STARTED";
})(IncidentActivityType = exports.IncidentActivityType || (exports.IncidentActivityType = {}));
var IncidentStatus;
(function (IncidentStatus) {
    IncidentStatus[IncidentStatus["OPENED"] = 1] = "OPENED";
    IncidentStatus[IncidentStatus["CLOSED"] = 2] = "CLOSED";
    IncidentStatus[IncidentStatus["WARNING"] = 10] = "WARNING";
    IncidentStatus[IncidentStatus["CRITICAL"] = 20] = "CRITICAL";
})(IncidentStatus = exports.IncidentStatus || (exports.IncidentStatus = {}));
var IncidentStatusMethod;
(function (IncidentStatusMethod) {
    IncidentStatusMethod[IncidentStatusMethod["MANUAL"] = 1] = "MANUAL";
    IncidentStatusMethod[IncidentStatusMethod["RULE_UPDATED"] = 2] = "RULE_UPDATED";
    IncidentStatusMethod[IncidentStatusMethod["RULE_TRIGGERED"] = 3] = "RULE_TRIGGERED";
})(IncidentStatusMethod = exports.IncidentStatusMethod || (exports.IncidentStatusMethod = {}));
var AlertRuleStatus;
(function (AlertRuleStatus) {
    AlertRuleStatus[AlertRuleStatus["PENDING"] = 0] = "PENDING";
    AlertRuleStatus[AlertRuleStatus["SNAPSHOT"] = 4] = "SNAPSHOT";
    AlertRuleStatus[AlertRuleStatus["DISABLED"] = 5] = "DISABLED";
})(AlertRuleStatus = exports.AlertRuleStatus || (exports.AlertRuleStatus = {}));
//# sourceMappingURL=types.jsx.map