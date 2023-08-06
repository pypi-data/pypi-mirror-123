Object.defineProperty(exports, "__esModule", { value: true });
exports.SourceSuggestionType = exports.EventIdStatus = exports.MethodType = exports.RuleType = void 0;
var RuleType;
(function (RuleType) {
    RuleType["PATTERN"] = "pattern";
    RuleType["CREDITCARD"] = "creditcard";
    RuleType["PASSWORD"] = "password";
    RuleType["IP"] = "ip";
    RuleType["IMEI"] = "imei";
    RuleType["EMAIL"] = "email";
    RuleType["UUID"] = "uuid";
    RuleType["PEMKEY"] = "pemkey";
    RuleType["URLAUTH"] = "url_auth";
    RuleType["USSSN"] = "us_ssn";
    RuleType["USER_PATH"] = "userpath";
    RuleType["MAC"] = "mac";
    RuleType["ANYTHING"] = "anything";
})(RuleType = exports.RuleType || (exports.RuleType = {}));
var MethodType;
(function (MethodType) {
    MethodType["MASK"] = "mask";
    MethodType["REMOVE"] = "remove";
    MethodType["HASH"] = "hash";
    MethodType["REPLACE"] = "replace";
})(MethodType = exports.MethodType || (exports.MethodType = {}));
var EventIdStatus;
(function (EventIdStatus) {
    EventIdStatus["UNDEFINED"] = "undefined";
    EventIdStatus["LOADING"] = "loading";
    EventIdStatus["INVALID"] = "invalid";
    EventIdStatus["NOT_FOUND"] = "not_found";
    EventIdStatus["LOADED"] = "loaded";
    EventIdStatus["ERROR"] = "error";
})(EventIdStatus = exports.EventIdStatus || (exports.EventIdStatus = {}));
var SourceSuggestionType;
(function (SourceSuggestionType) {
    SourceSuggestionType["VALUE"] = "value";
    SourceSuggestionType["UNARY"] = "unary";
    SourceSuggestionType["BINARY"] = "binary";
    SourceSuggestionType["STRING"] = "string";
})(SourceSuggestionType = exports.SourceSuggestionType || (exports.SourceSuggestionType = {}));
//# sourceMappingURL=types.jsx.map