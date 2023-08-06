Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const orderBy_1 = (0, tslib_1.__importDefault)(require("lodash/orderBy"));
const activityList_1 = (0, tslib_1.__importDefault)(require("./activityList"));
const cardHeader_1 = (0, tslib_1.__importDefault)(require("./cardHeader"));
const utils_1 = require("./utils");
const waitingActivity_1 = (0, tslib_1.__importDefault)(require("./waitingActivity"));
const List = ({ relays, relayActivities, onRefresh, onDelete, onEdit, disabled, }) => {
    const orderedRelays = (0, orderBy_1.default)(relays, relay => relay.created, ['desc']);
    const relaysByPublicKey = (0, utils_1.getRelaysByPublicKey)(orderedRelays, relayActivities);
    const renderCardContent = (activities) => {
        if (!activities.length) {
            return <waitingActivity_1.default onRefresh={onRefresh} disabled={disabled}/>;
        }
        return <activityList_1.default activities={activities}/>;
    };
    return (<div>
      {Object.keys(relaysByPublicKey).map(relayByPublicKey => {
            const { name, description, created, activities } = relaysByPublicKey[relayByPublicKey];
            return (<div key={relayByPublicKey}>
            <cardHeader_1.default publicKey={relayByPublicKey} name={name} description={description} created={created} onEdit={onEdit} onDelete={onDelete} disabled={disabled}/>
            {renderCardContent(activities)}
          </div>);
        })}
    </div>);
};
exports.default = List;
//# sourceMappingURL=index.jsx.map