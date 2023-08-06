#include "td_api.h"


void TdApi::CreateApi(const std::string &flow_path) {
    queue_ = new DispatchQueue();
    api_ = CThostFtdcTraderApi::CreateFtdcTraderApi(flow_path.c_str());
    api_->RegisterSpi(this);
}

std::string TdApi::GetApiVersion() {
    return CThostFtdcTraderApi::GetApiVersion();
}

void TdApi::Release() {
    api_->Release();
    delete queue_;
}

void TdApi::Init() {
    api_->Init();
}

int TdApi::Join() {
    return api_->Join();
}

std::string TdApi::GetTradingDay() {
    return api_->GetTradingDay();
}

void TdApi::RegisterFront(const std::string &front_address) {
    api_->RegisterFront(const_cast<char *>(front_address.c_str()));
}

// Req Methods
int TdApi::ReqAuthenticate(const py::dict &data, int request_id) {
    CThostFtdcReqAuthenticateField request{};
    strncpy(request.BrokerID, data["BrokerID"].cast<std::string>().c_str(), sizeof(request.BrokerID));
    strncpy(request.UserID, data["UserID"].cast<std::string>().c_str(), sizeof(request.UserID));
    strncpy(request.AuthCode, data["AuthCode"].cast<std::string>().c_str(), sizeof(request.AuthCode));
    strncpy(request.AppID, data["AppID"].cast<std::string>().c_str(), sizeof(request.AppID));
    return api_->ReqAuthenticate(&request, request_id);
}

int TdApi::ReqUserLogin(const py::dict &data, int request_id) {
    CThostFtdcReqUserLoginField request{};
    strncpy(request.BrokerID, data["BrokerID"].cast<std::string>().c_str(), sizeof(request.BrokerID));
    strncpy(request.UserID, data["UserID"].cast<std::string>().c_str(), sizeof(request.UserID));
    strncpy(request.Password, data["Password"].cast<std::string>().c_str(), sizeof(request.Password));
    return api_->ReqUserLogin(&request, request_id);
}

int TdApi::ReqUserLogout(const py::dict &data, int request_id) {
    CThostFtdcUserLogoutField request{};
    strncpy(request.BrokerID, data["BrokerID"].cast<std::string>().c_str(), sizeof(request.BrokerID));
    strncpy(request.UserID, data["UserID"].cast<std::string>().c_str(), sizeof(request.UserID));
    return api_->ReqUserLogout(&request, request_id);
}

int TdApi::ReqOrderInsert(const py::dict &data, int request_id) {
    CThostFtdcInputOrderField request{};
    // @todo: 整理参数
    strncpy(request.BrokerID, data["BrokerID"].cast<std::string>().c_str(), sizeof(request.BrokerID));
    strncpy(request.InvestorID, data["InvestorID"].cast<std::string>().c_str(), sizeof(request.InvestorID));
    strncpy(request.OrderRef, data["OrderRef"].cast<std::string>().c_str(), sizeof(request.OrderRef));
    strncpy(request.UserID, data["UserID"].cast<std::string>().c_str(), sizeof(request.UserID));
    request.OrderPriceType = data["OrderPriceType"].cast<char>();
    request.Direction = data["Direction"].cast<char>();
    strncpy(request.CombOffsetFlag, data["CombOffsetFlag"].cast<std::string>().c_str(), sizeof(request.CombOffsetFlag));
    strncpy(request.CombHedgeFlag, data["CombHedgeFlag"].cast<std::string>().c_str(), sizeof(request.CombHedgeFlag));
    request.LimitPrice = data["LimitPrice"].cast<double>();
    request.VolumeTotalOriginal = data["VolumeTotalOriginal"].cast<int>();
    request.TimeCondition = data["TimeCondition"].cast<char>();
    strncpy(request.GTDDate, data["GTDDate"].cast<std::string>().c_str(), sizeof(request.GTDDate));
    request.VolumeCondition = data["VolumeCondition"].cast<char>();
    // request.MinVolume = data["MinVolume"].cast<int>();
    request.MinVolume = 1;
    request.ContingentCondition = data["ContingentCondition"].cast<char>();
    request.StopPrice = data["StopPrice"].cast<double>();
    request.ForceCloseReason = data["ForceCloseReason"].cast<char>();
    request.IsAutoSuspend = data["IsAutoSuspend"].cast<int>();
    // strncpy(request.BusinessUnit, data["BusinessUnit"].cast<std::string>().c_str(), sizeof(request.BusinessUnit));
    request.RequestID = data["RequestID"].cast<int>();
    request.UserForceClose = data["UserForceClose"].cast<int>();
    request.IsSwapOrder = data["IsSwapOrder"].cast<int>();
    strncpy(request.ExchangeID, data["ExchangeID"].cast<std::string>().c_str(), sizeof(request.ExchangeID));
    // strncpy(request.InvestUnitID, data["InvestUnitID"].cast<std::string>().c_str(), sizeof(request.InvestUnitID));
    // strncpy(request.AccountID, data["AccountID"].cast<std::string>().c_str(), sizeof(request.AccountID));
    // strncpy(request.CurrencyID, data["CurrencyID"].cast<std::string>().c_str(), sizeof(request.CurrencyID));
    // strncpy(request.ClientID, data["ClientID"].cast<std::string>().c_str(), sizeof(request.ClientID));
    strncpy(request.MacAddress, data["MacAddress"].cast<std::string>().c_str(), sizeof(request.MacAddress));
    strncpy(request.InstrumentID, data["InstrumentID"].cast<std::string>().c_str(), sizeof(request.InstrumentID));
    // strncpy(request.IPAddress, data["IPAddress"].cast<std::string>().c_str(), sizeof(request.IPAddress));
    return api_->ReqOrderInsert(&request, request_id);
}

int TdApi::ReqOrderAction(const py::dict &data, int request_id) {
    CThostFtdcInputOrderActionField request{};
    request.SessionID = data["SessionID"].cast<int>();
    request.FrontID = data["FrontID"].cast<int>();
    strncpy(request.BrokerID, data["BrokerID"].cast<std::string>().c_str(), sizeof(request.BrokerID));
    strncpy(request.InvestorID, data["InvestorID"].cast<std::string>().c_str(), sizeof(request.InvestorID));
    strncpy(request.InstrumentID, data["InstrumentID"].cast<std::string>().c_str(), sizeof(request.InstrumentID));
    strncpy(request.ExchangeID, data["ExchangeID"].cast<std::string>().c_str(), sizeof(request.ExchangeID));
    strncpy(request.OrderRef, data["OrderRef"].cast<std::string>().c_str(), sizeof(request.OrderRef));
    request.ActionFlag = data["ActionFlag"].cast<char>();
    return api_->ReqOrderAction(&request, request_id);
}

int TdApi::ReqSettlementInfoConfirm(const py::dict &data, int request_id) {
    CThostFtdcSettlementInfoConfirmField request{};
    strncpy(request.BrokerID, data["BrokerID"].cast<std::string>().c_str(), sizeof(request.BrokerID));
    strncpy(request.InvestorID, data["InvestorID"].cast<std::string>().c_str(), sizeof(request.InvestorID));
    return api_->ReqSettlementInfoConfirm(&request, request_id);
}

int TdApi::ReqQryOrder(const py::dict &data, int request_id) {
    CThostFtdcQryOrderField request{};
    strncpy(request.BrokerID, data["BrokerID"].cast<std::string>().c_str(), sizeof(request.BrokerID));
    strncpy(request.InvestorID, data["InvestorID"].cast<std::string>().c_str(), sizeof(request.InvestorID));
    return api_->ReqQryOrder(&request, request_id);
}

int TdApi::ReqQryTrade(const py::dict &data, int request_id) {
    CThostFtdcQryTradeField request{};
    strncpy(request.BrokerID, data["BrokerID"].cast<std::string>().c_str(), sizeof(request.BrokerID));
    strncpy(request.InvestorID, data["InvestorID"].cast<std::string>().c_str(), sizeof(request.InvestorID));
    return api_->ReqQryTrade(&request, request_id);
}

int TdApi::ReqQryInvestorPosition(const py::dict &data, int request_id) {
    CThostFtdcQryInvestorPositionField request{};
    strncpy(request.BrokerID, data["BrokerID"].cast<std::string>().c_str(), sizeof(request.BrokerID));
    strncpy(request.InvestorID, data["InvestorID"].cast<std::string>().c_str(), sizeof(request.InvestorID));
    return api_->ReqQryInvestorPosition(&request, request_id);
}

int TdApi::ReqQryTradingAccount(const py::dict &data, int request_id) {
    CThostFtdcQryTradingAccountField request{};
    strncpy(request.BrokerID, data["BrokerID"].cast<std::string>().c_str(), sizeof(request.BrokerID));
    strncpy(request.InvestorID, data["InvestorID"].cast<std::string>().c_str(), sizeof(request.InvestorID));
    return api_->ReqQryTradingAccount(&request, request_id);
}

int TdApi::ReqQryInstrument(const py::dict &data, int request_id) {
    CThostFtdcQryInstrumentField request{};
    return api_->ReqQryInstrument(&request, request_id);
}

int TdApi::ReqQrySettlementInfo(const py::dict &data, int request_id) {
    CThostFtdcQrySettlementInfoField request{};
    strncpy(request.BrokerID, data["BrokerID"].cast<std::string>().c_str(), sizeof(request.BrokerID));
    strncpy(request.InvestorID, data["InvestorID"].cast<std::string>().c_str(), sizeof(request.InvestorID));
    return api_->ReqQrySettlementInfo(&request, request_id);
}

// On Methods
void TdApi::OnFrontConnected() {
    queue_->dispatch([&]() {
        py::gil_scoped_acquire acquire;
        this->PyOnFrontConnected();
    });
}

void TdApi::OnFrontDisconnected(int reason) {
    queue_->dispatch([&]() {
        py::gil_scoped_acquire acquire;
        this->PyOnFrontDisconnected(reason);
    });
}

void TdApi::OnHeartBeatWarning(int time_lapse) {
    queue_->dispatch([&]() {
        py::gil_scoped_acquire acquire;
        this->PyOnHeartBeatWarning(time_lapse);
    });
}

void TdApi::OnRspAuthenticate(CThostFtdcRspAuthenticateField *pRspAuthenticateField, CThostFtdcRspInfoField *pRspInfo, int request_id, bool is_last) {
    queue_->dispatch([&]() {
        py::gil_scoped_acquire acquire;

        py::dict data;
        if (pRspAuthenticateField) {
            data["BrokerID"] = gb2312_to_utf8(pRspAuthenticateField->BrokerID);
            data["UserID"] = gb2312_to_utf8(pRspAuthenticateField->UserID);
            data["UserProductInfo"] = gb2312_to_utf8(pRspAuthenticateField->UserProductInfo);
            data["AppID"] = gb2312_to_utf8(pRspAuthenticateField->AppID);
            data["AppType"] = pRspAuthenticateField->AppType;
        }

        py::dict error;
        if (pRspInfo) {
            error["ErrorID"] = pRspInfo->ErrorID;
            error["ErrorMsg"] = gb2312_to_utf8(pRspInfo->ErrorMsg);
        }

        this->PyOnRspAuthenticate(data, error, request_id, is_last);
    });
}

void TdApi::OnRspUserLogin(CThostFtdcRspUserLoginField *pRspUserLogin, CThostFtdcRspInfoField *pRspInfo, int request_id, bool is_last) {
    queue_->dispatch([&]() {
        py::gil_scoped_acquire acquire;

        py::dict data;
        if (pRspUserLogin) {
            data["TradingDay"] = gb2312_to_utf8(pRspUserLogin->TradingDay);
            data["LoginTime"] = gb2312_to_utf8(pRspUserLogin->LoginTime);
            data["BrokerID"] = gb2312_to_utf8(pRspUserLogin->BrokerID);
            data["UserID"] = gb2312_to_utf8(pRspUserLogin->UserID);
            data["SystemName"] = gb2312_to_utf8(pRspUserLogin->SystemName);
            data["FrontID"] = pRspUserLogin->FrontID;
            data["SessionID"] = pRspUserLogin->SessionID;
            data["MaxOrderRef"] = gb2312_to_utf8(pRspUserLogin->MaxOrderRef);
            data["SHFETime"] = gb2312_to_utf8(pRspUserLogin->SHFETime);
            data["DCETime"] = gb2312_to_utf8(pRspUserLogin->DCETime);
            data["CZCETime"] = gb2312_to_utf8(pRspUserLogin->CZCETime);
            data["FFEXTime"] = gb2312_to_utf8(pRspUserLogin->FFEXTime);
            data["INETime"] = gb2312_to_utf8(pRspUserLogin->INETime);
        }

        py::dict error;
        if (pRspInfo) {
            error["ErrorID"] = pRspInfo->ErrorID;
            error["ErrorMsg"] = gb2312_to_utf8(pRspInfo->ErrorMsg);
        }

        this->PyOnRspUserLogin(data, error, request_id, is_last);
    });
}

void TdApi::OnRspUserLogout(CThostFtdcUserLogoutField *pUserLogout, CThostFtdcRspInfoField *pRspInfo, int request_id, bool is_last) {
    queue_->dispatch([&]() {
        py::gil_scoped_acquire acquire;

        py::dict data;
        if (pUserLogout) {
            data["BrokerID"] = gb2312_to_utf8(pUserLogout->BrokerID);
            data["UserID"] = gb2312_to_utf8(pUserLogout->UserID);
        }

        py::dict error;
        if (pRspInfo) {
            error["ErrorID"] = pRspInfo->ErrorID;
            error["ErrorMsg"] = gb2312_to_utf8(pRspInfo->ErrorMsg);
        }

        this->PyOnRspUserLogout(data, error, request_id, is_last);
    });
}

void TdApi::OnRspOrderInsert(CThostFtdcInputOrderField *pInputOrder, CThostFtdcRspInfoField *pRspInfo, int request_id, bool is_last) {
    queue_->dispatch([&]() {
        py::gil_scoped_acquire acquire;

        py::dict data;
        if (pInputOrder) {
            data["BrokerID"] = gb2312_to_utf8(pInputOrder->BrokerID);
            data["InvestorID"] = gb2312_to_utf8(pInputOrder->InvestorID);
            data["OrderRef"] = gb2312_to_utf8(pInputOrder->OrderRef);
            data["UserID"] = gb2312_to_utf8(pInputOrder->UserID);
            data["OrderPriceType"] = pInputOrder->OrderPriceType;
            data["Direction"] = pInputOrder->Direction;
            data["CombOffsetFlag"] = gb2312_to_utf8(pInputOrder->CombOffsetFlag);
            data["CombHedgeFlag"] = gb2312_to_utf8(pInputOrder->CombHedgeFlag);
            data["LimitPrice"] = pInputOrder->LimitPrice;
            data["VolumeTotalOriginal"] = pInputOrder->VolumeTotalOriginal;
            data["TimeCondition"] = pInputOrder->TimeCondition;
            data["GTDDate"] = gb2312_to_utf8(pInputOrder->GTDDate);
            data["VolumeCondition"] = pInputOrder->VolumeCondition;
            data["MinVolume"] = pInputOrder->MinVolume;
            data["ContingentCondition"] = pInputOrder->ContingentCondition;
            data["StopPrice"] = pInputOrder->StopPrice;
            data["ForceCloseReason"] = pInputOrder->ForceCloseReason;
            data["IsAutoSuspend"] = pInputOrder->IsAutoSuspend;
            data["BusinessUnit"] = gb2312_to_utf8(pInputOrder->BusinessUnit);
            data["RequestID"] = pInputOrder->RequestID;
            data["UserForceClose"] = pInputOrder->UserForceClose;
            data["IsSwapOrder"] = pInputOrder->IsSwapOrder;
            data["ExchangeID"] = gb2312_to_utf8(pInputOrder->ExchangeID);
            data["InvestUnitID"] = gb2312_to_utf8(pInputOrder->InvestUnitID);
            data["AccountID"] = gb2312_to_utf8(pInputOrder->AccountID);
            data["CurrencyID"] = gb2312_to_utf8(pInputOrder->CurrencyID);
            data["ClientID"] = gb2312_to_utf8(pInputOrder->ClientID);
            data["MacAddress"] = gb2312_to_utf8(pInputOrder->MacAddress);
            data["InstrumentID"] = gb2312_to_utf8(pInputOrder->InstrumentID);
            data["IPAddress"] = gb2312_to_utf8(pInputOrder->IPAddress);
        }

        py::dict error;
        if (pRspInfo) {
            error["ErrorID"] = pRspInfo->ErrorID;
            error["ErrorMsg"] = gb2312_to_utf8(pRspInfo->ErrorMsg);
        }

        this->PyOnRspOrderInsert(data, error, request_id, is_last);
    });
}

void TdApi::OnRspOrderAction(CThostFtdcInputOrderActionField *pInputOrderAction, CThostFtdcRspInfoField *pRspInfo, int request_id, bool is_last) {
    queue_->dispatch([&]() {
        py::gil_scoped_acquire acquire;

        py::dict data;
        if (pInputOrderAction) {
            data["BrokerID"] = gb2312_to_utf8(pInputOrderAction->BrokerID);
            data["InvestorID"] = gb2312_to_utf8(pInputOrderAction->InvestorID);
            data["OrderActionRef"] = pInputOrderAction->OrderActionRef;
            data["OrderRef"] = gb2312_to_utf8(pInputOrderAction->OrderRef);
            data["RequestID"] = pInputOrderAction->RequestID;
            data["FrontID"] = pInputOrderAction->FrontID;
            data["SessionID"] = pInputOrderAction->SessionID;
            data["ExchangeID"] = gb2312_to_utf8(pInputOrderAction->ExchangeID);
            data["OrderSysID"] = gb2312_to_utf8(pInputOrderAction->OrderSysID);
            data["ActionFlag"] = pInputOrderAction->ActionFlag;
            data["LimitPrice"] = pInputOrderAction->LimitPrice;
            data["VolumeChange"] = pInputOrderAction->VolumeChange;
            data["UserID"] = gb2312_to_utf8(pInputOrderAction->UserID);
            data["InvestUnitID"] = gb2312_to_utf8(pInputOrderAction->InvestUnitID);
            data["MacAddress"] = gb2312_to_utf8(pInputOrderAction->MacAddress);
            data["InstrumentID"] = gb2312_to_utf8(pInputOrderAction->InstrumentID);
            data["IPAddress"] = gb2312_to_utf8(pInputOrderAction->IPAddress);
        }

        py::dict error;
        if (pRspInfo) {
            error["ErrorID"] = pRspInfo->ErrorID;
            error["ErrorMsg"] = gb2312_to_utf8(pRspInfo->ErrorMsg);
        }

        this->PyOnRspOrderAction(data, error, request_id, is_last);
    });
}

void TdApi::OnRspSettlementInfoConfirm(CThostFtdcSettlementInfoConfirmField *pSettlementInfoConfirm, CThostFtdcRspInfoField *pRspInfo, int request_id, bool is_last) {
    queue_->dispatch([&]() {
        py::gil_scoped_acquire acquire;

        py::dict data;
        if (pSettlementInfoConfirm) {
            data["BrokerID"] = gb2312_to_utf8(pSettlementInfoConfirm->BrokerID);
            data["InvestorID"] = gb2312_to_utf8(pSettlementInfoConfirm->InvestorID);
            data["ConfirmDate"] = gb2312_to_utf8(pSettlementInfoConfirm->ConfirmDate);
            data["ConfirmTime"] = gb2312_to_utf8(pSettlementInfoConfirm->ConfirmTime);
            data["SettlementID"] = pSettlementInfoConfirm->SettlementID;
            data["AccountID"] = gb2312_to_utf8(pSettlementInfoConfirm->AccountID);
            data["CurrencyID"] = gb2312_to_utf8(pSettlementInfoConfirm->CurrencyID);
        }

        py::dict error;
        if (pRspInfo) {
            error["ErrorID"] = pRspInfo->ErrorID;
            error["ErrorMsg"] = gb2312_to_utf8(pRspInfo->ErrorMsg);
        }

        this->PyOnRspSettlementInfoConfirm(data, error, request_id, is_last);
    });
}

void TdApi::OnRspQryOrder(CThostFtdcOrderField *pOrder, CThostFtdcRspInfoField *pRspInfo, int request_id, bool is_last) {
    queue_->dispatch([&]() {
        py::gil_scoped_acquire acquire;

        py::dict data;
        if (pOrder) {
            data["BrokerID"] = gb2312_to_utf8(pOrder->BrokerID);
            data["InvestorID"] = gb2312_to_utf8(pOrder->InvestorID);
            data["OrderRef"] = gb2312_to_utf8(pOrder->OrderRef);
            data["UserID"] = gb2312_to_utf8(pOrder->UserID);
            data["OrderPriceType"] = pOrder->OrderPriceType;
            data["Direction"] = pOrder->Direction;
            data["CombOffsetFlag"] = gb2312_to_utf8(pOrder->CombOffsetFlag);
            data["CombHedgeFlag"] = gb2312_to_utf8(pOrder->CombHedgeFlag);
            data["LimitPrice"] = pOrder->LimitPrice;
            data["VolumeTotalOriginal"] = pOrder->VolumeTotalOriginal;
            data["TimeCondition"] = pOrder->TimeCondition;
            data["GTDDate"] = gb2312_to_utf8(pOrder->GTDDate);
            data["VolumeCondition"] = pOrder->VolumeCondition;
            data["MinVolume"] = pOrder->MinVolume;
            data["ContingentCondition"] = pOrder->ContingentCondition;
            data["StopPrice"] = pOrder->StopPrice;
            data["ForceCloseReason"] = pOrder->ForceCloseReason;
            data["IsAutoSuspend"] = pOrder->IsAutoSuspend;
            data["BusinessUnit"] = gb2312_to_utf8(pOrder->BusinessUnit);
            data["RequestID"] = pOrder->RequestID;
            data["OrderLocalID"] = gb2312_to_utf8(pOrder->OrderLocalID);
            data["ExchangeID"] = gb2312_to_utf8(pOrder->ExchangeID);
            data["ParticipantID"] = gb2312_to_utf8(pOrder->ParticipantID);
            data["ClientID"] = gb2312_to_utf8(pOrder->ClientID);
            data["TraderID"] = gb2312_to_utf8(pOrder->TraderID);
            data["InstallID"] = pOrder->InstallID;
            data["OrderSubmitStatus"] = pOrder->OrderSubmitStatus;
            data["NotifySequence"] = pOrder->NotifySequence;
            data["TradingDay"] = gb2312_to_utf8(pOrder->TradingDay);
            data["SettlementID"] = pOrder->SettlementID;
            data["OrderSysID"] = gb2312_to_utf8(pOrder->OrderSysID);
            data["OrderSource"] = pOrder->OrderSource;
            data["OrderStatus"] = pOrder->OrderStatus;
            data["OrderType"] = pOrder->OrderType;
            data["VolumeTraded"] = pOrder->VolumeTraded;
            data["VolumeTotal"] = pOrder->VolumeTotal;
            data["InsertDate"] = gb2312_to_utf8(pOrder->InsertDate);
            data["InsertTime"] = gb2312_to_utf8(pOrder->InsertTime);
            data["ActiveTime"] = gb2312_to_utf8(pOrder->ActiveTime);
            data["SuspendTime"] = gb2312_to_utf8(pOrder->SuspendTime);
            data["UpdateTime"] = gb2312_to_utf8(pOrder->UpdateTime);
            data["CancelTime"] = gb2312_to_utf8(pOrder->CancelTime);
            data["ActiveTraderID"] = gb2312_to_utf8(pOrder->ActiveTraderID);
            data["ClearingPartID"] = gb2312_to_utf8(pOrder->ClearingPartID);
            data["SequenceNo"] = pOrder->SequenceNo;
            data["FrontID"] = pOrder->FrontID;
            data["SessionID"] = pOrder->SessionID;
            data["UserProductInfo"] = gb2312_to_utf8(pOrder->UserProductInfo);
            data["StatusMsg"] = gb2312_to_utf8(pOrder->StatusMsg);
            data["UserForceClose"] = pOrder->UserForceClose;
            data["ActiveUserID"] = gb2312_to_utf8(pOrder->ActiveUserID);
            data["BrokerOrderSeq"] = pOrder->BrokerOrderSeq;
            data["RelativeOrderSysID"] = gb2312_to_utf8(pOrder->RelativeOrderSysID);
            data["ZCETotalTradedVolume"] = pOrder->ZCETotalTradedVolume;
            data["IsSwapOrder"] = pOrder->IsSwapOrder;
            data["BranchID"] = gb2312_to_utf8(pOrder->BranchID);
            data["InvestUnitID"] = gb2312_to_utf8(pOrder->InvestUnitID);
            data["AccountID"] = gb2312_to_utf8(pOrder->AccountID);
            data["CurrencyID"] = gb2312_to_utf8(pOrder->CurrencyID);
            data["MacAddress"] = gb2312_to_utf8(pOrder->MacAddress);
            data["InstrumentID"] = gb2312_to_utf8(pOrder->InstrumentID);
            data["ExchangeInstID"] = gb2312_to_utf8(pOrder->ExchangeInstID);
            data["IPAddress"] = gb2312_to_utf8(pOrder->IPAddress);
        }

        py::dict error;
        if (pRspInfo) {
            error["ErrorID"] = pRspInfo->ErrorID;
            error["ErrorMsg"] = gb2312_to_utf8(pRspInfo->ErrorMsg);
        }

        this->PyOnRspQryOrder(data, error, request_id, is_last);
    });
}

void TdApi::OnRspQryTrade(CThostFtdcTradeField *pTrade, CThostFtdcRspInfoField *pRspInfo, int request_id, bool is_last) {
    queue_->dispatch([&]() {
        py::gil_scoped_acquire acquire;

        py::dict data;
        if (pTrade) {
            data["BrokerID"] = gb2312_to_utf8(pTrade->BrokerID);
            data["InvestorID"] = gb2312_to_utf8(pTrade->InvestorID);
            data["OrderRef"] = gb2312_to_utf8(pTrade->OrderRef);
            data["UserID"] = gb2312_to_utf8(pTrade->UserID);
            data["ExchangeID"] = gb2312_to_utf8(pTrade->ExchangeID);
            data["TradeID"] = gb2312_to_utf8(pTrade->TradeID);
            data["Direction"] = pTrade->Direction;
            data["OrderSysID"] = gb2312_to_utf8(pTrade->OrderSysID);
            data["ParticipantID"] = gb2312_to_utf8(pTrade->ParticipantID);
            data["ClientID"] = gb2312_to_utf8(pTrade->ClientID);
            data["TradingRole"] = pTrade->TradingRole;
            data["OffsetFlag"] = pTrade->OffsetFlag;
            data["HedgeFlag"] = pTrade->HedgeFlag;
            data["Price"] = pTrade->Price;
            data["Volume"] = pTrade->Volume;
            data["TradeDate"] = gb2312_to_utf8(pTrade->TradeDate);
            data["TradeTime"] = gb2312_to_utf8(pTrade->TradeTime);
            data["TradeType"] = pTrade->TradeType;
            data["PriceSource"] = pTrade->PriceSource;
            data["TraderID"] = gb2312_to_utf8(pTrade->TraderID);
            data["OrderLocalID"] = gb2312_to_utf8(pTrade->OrderLocalID);
            data["ClearingPartID"] = gb2312_to_utf8(pTrade->ClearingPartID);
            data["BusinessUnit"] = gb2312_to_utf8(pTrade->BusinessUnit);
            data["SequenceNo"] = pTrade->SequenceNo;
            data["TradingDay"] = gb2312_to_utf8(pTrade->TradingDay);
            data["SettlementID"] = pTrade->SettlementID;
            data["BrokerOrderSeq"] = pTrade->BrokerOrderSeq;
            data["TradeSource"] = pTrade->TradeSource;
            data["InvestUnitID"] = gb2312_to_utf8(pTrade->InvestUnitID);
            data["InstrumentID"] = gb2312_to_utf8(pTrade->InstrumentID);
            data["ExchangeInstID"] = gb2312_to_utf8(pTrade->ExchangeInstID);
        }

        py::dict error;
        if (pRspInfo) {
            error["ErrorID"] = pRspInfo->ErrorID;
            error["ErrorMsg"] = gb2312_to_utf8(pRspInfo->ErrorMsg);
        }

        this->PyOnRspQryTrade(data, error, request_id, is_last);
    });
}

void TdApi::OnRspQryInvestorPosition(CThostFtdcInvestorPositionField *pInvestorPosition, CThostFtdcRspInfoField *pRspInfo, int request_id, bool is_last) {
    queue_->dispatch([&]() {
        py::gil_scoped_acquire acquire;

        py::dict data;
        if (pInvestorPosition) {
            data["BrokerID"] = gb2312_to_utf8(pInvestorPosition->BrokerID);
            data["InvestorID"] = gb2312_to_utf8(pInvestorPosition->InvestorID);
            data["PosiDirection"] = pInvestorPosition->PosiDirection;
            data["HedgeFlag"] = pInvestorPosition->HedgeFlag;
            data["PositionDate"] = pInvestorPosition->PositionDate;
            data["YdPosition"] = pInvestorPosition->YdPosition;
            data["Position"] = pInvestorPosition->Position;
            data["LongFrozen"] = pInvestorPosition->LongFrozen;
            data["ShortFrozen"] = pInvestorPosition->ShortFrozen;
            data["LongFrozenAmount"] = pInvestorPosition->LongFrozenAmount;
            data["ShortFrozenAmount"] = pInvestorPosition->ShortFrozenAmount;
            data["OpenVolume"] = pInvestorPosition->OpenVolume;
            data["CloseVolume"] = pInvestorPosition->CloseVolume;
            data["OpenAmount"] = pInvestorPosition->OpenAmount;
            data["CloseAmount"] = pInvestorPosition->CloseAmount;
            data["PositionCost"] = pInvestorPosition->PositionCost;
            data["PreMargin"] = pInvestorPosition->PreMargin;
            data["UseMargin"] = pInvestorPosition->UseMargin;
            data["FrozenMargin"] = pInvestorPosition->FrozenMargin;
            data["FrozenCash"] = pInvestorPosition->FrozenCash;
            data["FrozenCommission"] = pInvestorPosition->FrozenCommission;
            data["CashIn"] = pInvestorPosition->CashIn;
            data["Commission"] = pInvestorPosition->Commission;
            data["CloseProfit"] = pInvestorPosition->CloseProfit;
            data["PositionProfit"] = pInvestorPosition->PositionProfit;
            data["PreSettlementPrice"] = pInvestorPosition->PreSettlementPrice;
            data["SettlementPrice"] = pInvestorPosition->SettlementPrice;
            data["TradingDay"] = gb2312_to_utf8(pInvestorPosition->TradingDay);
            data["SettlementID"] = pInvestorPosition->SettlementID;
            data["OpenCost"] = pInvestorPosition->OpenCost;
            data["ExchangeMargin"] = pInvestorPosition->ExchangeMargin;
            data["CombPosition"] = pInvestorPosition->CombPosition;
            data["CombLongFrozen"] = pInvestorPosition->CombLongFrozen;
            data["CombShortFrozen"] = pInvestorPosition->CombShortFrozen;
            data["CloseProfitByDate"] = pInvestorPosition->CloseProfitByDate;
            data["CloseProfitByTrade"] = pInvestorPosition->CloseProfitByTrade;
            data["TodayPosition"] = pInvestorPosition->TodayPosition;
            data["MarginRateByMoney"] = pInvestorPosition->MarginRateByMoney;
            data["MarginRateByVolume"] = pInvestorPosition->MarginRateByVolume;
            data["StrikeFrozen"] = pInvestorPosition->StrikeFrozen;
            data["StrikeFrozenAmount"] = pInvestorPosition->StrikeFrozenAmount;
            data["AbandonFrozen"] = pInvestorPosition->AbandonFrozen;
            data["ExchangeID"] = gb2312_to_utf8(pInvestorPosition->ExchangeID);
            data["YdStrikeFrozen"] = pInvestorPosition->YdStrikeFrozen;
            data["InvestUnitID"] = gb2312_to_utf8(pInvestorPosition->InvestUnitID);
            data["PositionCostOffset"] = pInvestorPosition->PositionCostOffset;
            data["TasPosition"] = pInvestorPosition->TasPosition;
            data["TasPositionCost"] = pInvestorPosition->TasPositionCost;
            data["InstrumentID"] = gb2312_to_utf8(pInvestorPosition->InstrumentID);
        }

        py::dict error;
        if (pRspInfo) {
            error["ErrorID"] = pRspInfo->ErrorID;
            error["ErrorMsg"] = gb2312_to_utf8(pRspInfo->ErrorMsg);
        }

        this->PyOnRspQryInvestorPosition(data, error, request_id, is_last);
    });
}

void TdApi::OnRspQryTradingAccount(CThostFtdcTradingAccountField *pTradingAccount, CThostFtdcRspInfoField *pRspInfo, int request_id, bool is_last) {
    queue_->dispatch([&]() {
        py::gil_scoped_acquire acquire;

        py::dict data;
        if (pTradingAccount) {
            data["BrokerID"] = gb2312_to_utf8(pTradingAccount->BrokerID);
            data["AccountID"] = gb2312_to_utf8(pTradingAccount->AccountID);
            data["PreMortgage"] = pTradingAccount->PreMortgage;
            data["PreCredit"] = pTradingAccount->PreCredit;
            data["PreDeposit"] = pTradingAccount->PreDeposit;
            data["PreBalance"] = pTradingAccount->PreBalance;
            data["PreMargin"] = pTradingAccount->PreMargin;
            data["InterestBase"] = pTradingAccount->InterestBase;
            data["Interest"] = pTradingAccount->Interest;
            data["Deposit"] = pTradingAccount->Deposit;
            data["Withdraw"] = pTradingAccount->Withdraw;
            data["FrozenMargin"] = pTradingAccount->FrozenMargin;
            data["FrozenCash"] = pTradingAccount->FrozenCash;
            data["FrozenCommission"] = pTradingAccount->FrozenCommission;
            data["CurrMargin"] = pTradingAccount->CurrMargin;
            data["CashIn"] = pTradingAccount->CashIn;
            data["Commission"] = pTradingAccount->Commission;
            data["CloseProfit"] = pTradingAccount->CloseProfit;
            data["PositionProfit"] = pTradingAccount->PositionProfit;
            data["Balance"] = pTradingAccount->Balance;
            data["Available"] = pTradingAccount->Available;
            data["WithdrawQuota"] = pTradingAccount->WithdrawQuota;
            data["Reserve"] = pTradingAccount->Reserve;
            data["TradingDay"] = gb2312_to_utf8(pTradingAccount->TradingDay);
            data["SettlementID"] = pTradingAccount->SettlementID;
            data["Credit"] = pTradingAccount->Credit;
            data["Mortgage"] = pTradingAccount->Mortgage;
            data["ExchangeMargin"] = pTradingAccount->ExchangeMargin;
            data["DeliveryMargin"] = pTradingAccount->DeliveryMargin;
            data["ExchangeDeliveryMargin"] = pTradingAccount->ExchangeDeliveryMargin;
            data["ReserveBalance"] = pTradingAccount->ReserveBalance;
            data["CurrencyID"] = gb2312_to_utf8(pTradingAccount->CurrencyID);
            data["PreFundMortgageIn"] = pTradingAccount->PreFundMortgageIn;
            data["PreFundMortgageOut"] = pTradingAccount->PreFundMortgageOut;
            data["FundMortgageIn"] = pTradingAccount->FundMortgageIn;
            data["FundMortgageOut"] = pTradingAccount->FundMortgageOut;
            data["FundMortgageAvailable"] = pTradingAccount->FundMortgageAvailable;
            data["MortgageableFund"] = pTradingAccount->MortgageableFund;
            data["SpecProductMargin"] = pTradingAccount->SpecProductMargin;
            data["SpecProductFrozenMargin"] = pTradingAccount->SpecProductFrozenMargin;
            data["SpecProductCommission"] = pTradingAccount->SpecProductCommission;
            data["SpecProductFrozenCommission"] = pTradingAccount->SpecProductFrozenCommission;
            data["SpecProductPositionProfit"] = pTradingAccount->SpecProductPositionProfit;
            data["SpecProductCloseProfit"] = pTradingAccount->SpecProductCloseProfit;
            data["SpecProductPositionProfitByAlg"] = pTradingAccount->SpecProductPositionProfitByAlg;
            data["SpecProductExchangeMargin"] = pTradingAccount->SpecProductExchangeMargin;
            data["BizType"] = pTradingAccount->BizType;
            data["FrozenSwap"] = pTradingAccount->FrozenSwap;
            data["RemainSwap"] = pTradingAccount->RemainSwap;
        }

        py::dict error;
        if (pRspInfo) {
            error["ErrorID"] = pRspInfo->ErrorID;
            error["ErrorMsg"] = gb2312_to_utf8(pRspInfo->ErrorMsg);
        }

        this->PyOnRspQryTradingAccount(data, error, request_id, is_last);
    });
}

void TdApi::OnRspQryInstrument(CThostFtdcInstrumentField *pInstrument, CThostFtdcRspInfoField *pRspInfo, int request_id, bool is_last) {
    queue_->dispatch([&]() {
        py::gil_scoped_acquire acquire;

        py::dict data;
        if (pInstrument) {
            data["ExchangeID"] = gb2312_to_utf8(pInstrument->ExchangeID);
            data["InstrumentName"] = gb2312_to_utf8(pInstrument->InstrumentName);
            data["ProductClass"] = pInstrument->ProductClass;
            data["DeliveryYear"] = pInstrument->DeliveryYear;
            data["DeliveryMonth"] = pInstrument->DeliveryMonth;
            data["MaxMarketOrderVolume"] = pInstrument->MaxMarketOrderVolume;
            data["MinMarketOrderVolume"] = pInstrument->MinMarketOrderVolume;
            data["MaxLimitOrderVolume"] = pInstrument->MaxLimitOrderVolume;
            data["MinLimitOrderVolume"] = pInstrument->MinLimitOrderVolume;
            data["VolumeMultiple"] = pInstrument->VolumeMultiple;
            data["PriceTick"] = pInstrument->PriceTick;
            data["CreateDate"] = gb2312_to_utf8(pInstrument->CreateDate);
            data["OpenDate"] = gb2312_to_utf8(pInstrument->OpenDate);
            data["ExpireDate"] = gb2312_to_utf8(pInstrument->ExpireDate);
            data["StartDelivDate"] = gb2312_to_utf8(pInstrument->StartDelivDate);
            data["EndDelivDate"] = gb2312_to_utf8(pInstrument->EndDelivDate);
            data["InstLifePhase"] = pInstrument->InstLifePhase;
            data["IsTrading"] = pInstrument->IsTrading;
            data["PositionType"] = pInstrument->PositionType;
            data["PositionDateType"] = pInstrument->PositionDateType;
            data["LongMarginRatio"] = pInstrument->LongMarginRatio;
            data["ShortMarginRatio"] = pInstrument->ShortMarginRatio;
            data["MaxMarginSideAlgorithm"] = pInstrument->MaxMarginSideAlgorithm;
            data["StrikePrice"] = pInstrument->StrikePrice;
            data["OptionsType"] = pInstrument->OptionsType;
            data["UnderlyingMultiple"] = pInstrument->UnderlyingMultiple;
            data["CombinationType"] = pInstrument->CombinationType;
            data["InstrumentID"] = gb2312_to_utf8(pInstrument->InstrumentID);
            data["ExchangeInstID"] = gb2312_to_utf8(pInstrument->ExchangeInstID);
            data["ProductID"] = gb2312_to_utf8(pInstrument->ProductID);
            data["UnderlyingInstrID"] = gb2312_to_utf8(pInstrument->UnderlyingInstrID);
        }

        py::dict error;
        if (pRspInfo) {
            error["ErrorID"] = pRspInfo->ErrorID;
            error["ErrorMsg"] = gb2312_to_utf8(pRspInfo->ErrorMsg);
        }

        this->PyOnRspQryInstrument(data, error, request_id, is_last);
    });
}

void TdApi::OnRspQrySettlementInfo(CThostFtdcSettlementInfoField *pSettlementInfo, CThostFtdcRspInfoField *pRspInfo, int request_id, bool is_last) {
    queue_->dispatch([&]() {
        py::gil_scoped_acquire acquire;

        py::dict data;
        if (pSettlementInfo) {
            data["TradingDay"] = gb2312_to_utf8(pSettlementInfo->TradingDay);
            data["SettlementID"] = pSettlementInfo->SettlementID;
            data["BrokerID"] = gb2312_to_utf8(pSettlementInfo->BrokerID);
            data["InvestorID"] = gb2312_to_utf8(pSettlementInfo->InvestorID);
            data["SequenceNo"] = pSettlementInfo->SequenceNo;
            data["Content"] = gb2312_to_utf8(pSettlementInfo->Content);
            data["AccountID"] = gb2312_to_utf8(pSettlementInfo->AccountID);
            data["CurrencyID"] = gb2312_to_utf8(pSettlementInfo->CurrencyID);
        }

        py::dict error;
        if (pRspInfo) {
            error["ErrorID"] = pRspInfo->ErrorID;
            error["ErrorMsg"] = gb2312_to_utf8(pRspInfo->ErrorMsg);
        }

        this->PyOnRspQrySettlementInfo(data, error, request_id, is_last);
    });
}

void TdApi::OnRspError(CThostFtdcRspInfoField *pRspInfo, int request_id, bool is_last) {
    queue_->dispatch([&]() {
        py::gil_scoped_acquire acquire;
        py::dict error;
        if (pRspInfo) {
            error["ErrorID"] = pRspInfo->ErrorID;
            error["ErrorMsg"] = gb2312_to_utf8(pRspInfo->ErrorMsg);
        }
        this->PyOnRspError(error, request_id, is_last);
    });
}

void TdApi::OnRtnOrder(CThostFtdcOrderField *pOrder) {
    queue_->dispatch([&]() {
        py::gil_scoped_acquire acquire;
        py::dict data;
        if (pOrder) {
            data["BrokerID"] = gb2312_to_utf8(pOrder->BrokerID);
            data["InvestorID"] = gb2312_to_utf8(pOrder->InvestorID);
            data["OrderRef"] = gb2312_to_utf8(pOrder->OrderRef);
            data["UserID"] = gb2312_to_utf8(pOrder->UserID);
            data["OrderPriceType"] = pOrder->OrderPriceType;
            data["Direction"] = pOrder->Direction;
            data["CombOffsetFlag"] = gb2312_to_utf8(pOrder->CombOffsetFlag);
            data["CombHedgeFlag"] = gb2312_to_utf8(pOrder->CombHedgeFlag);
            data["LimitPrice"] = pOrder->LimitPrice;
            data["VolumeTotalOriginal"] = pOrder->VolumeTotalOriginal;
            data["TimeCondition"] = pOrder->TimeCondition;
            data["GTDDate"] = gb2312_to_utf8(pOrder->GTDDate);
            data["VolumeCondition"] = pOrder->VolumeCondition;
            data["MinVolume"] = pOrder->MinVolume;
            data["ContingentCondition"] = pOrder->ContingentCondition;
            data["StopPrice"] = pOrder->StopPrice;
            data["ForceCloseReason"] = pOrder->ForceCloseReason;
            data["IsAutoSuspend"] = pOrder->IsAutoSuspend;
            data["BusinessUnit"] = gb2312_to_utf8(pOrder->BusinessUnit);
            data["RequestID"] = pOrder->RequestID;
            data["OrderLocalID"] = gb2312_to_utf8(pOrder->OrderLocalID);
            data["ExchangeID"] = gb2312_to_utf8(pOrder->ExchangeID);
            data["ParticipantID"] = gb2312_to_utf8(pOrder->ParticipantID);
            data["ClientID"] = gb2312_to_utf8(pOrder->ClientID);
            data["TraderID"] = gb2312_to_utf8(pOrder->TraderID);
            data["InstallID"] = pOrder->InstallID;
            data["OrderSubmitStatus"] = pOrder->OrderSubmitStatus;
            data["NotifySequence"] = pOrder->NotifySequence;
            data["TradingDay"] = gb2312_to_utf8(pOrder->TradingDay);
            data["SettlementID"] = pOrder->SettlementID;
            data["OrderSysID"] = gb2312_to_utf8(pOrder->OrderSysID);
            data["OrderSource"] = pOrder->OrderSource;
            data["OrderStatus"] = pOrder->OrderStatus;
            data["OrderType"] = pOrder->OrderType;
            data["VolumeTraded"] = pOrder->VolumeTraded;
            data["VolumeTotal"] = pOrder->VolumeTotal;
            data["InsertDate"] = gb2312_to_utf8(pOrder->InsertDate);
            data["InsertTime"] = gb2312_to_utf8(pOrder->InsertTime);
            data["ActiveTime"] = gb2312_to_utf8(pOrder->ActiveTime);
            data["SuspendTime"] = gb2312_to_utf8(pOrder->SuspendTime);
            data["UpdateTime"] = gb2312_to_utf8(pOrder->UpdateTime);
            data["CancelTime"] = gb2312_to_utf8(pOrder->CancelTime);
            data["ActiveTraderID"] = gb2312_to_utf8(pOrder->ActiveTraderID);
            data["ClearingPartID"] = gb2312_to_utf8(pOrder->ClearingPartID);
            data["SequenceNo"] = pOrder->SequenceNo;
            data["FrontID"] = pOrder->FrontID;
            data["SessionID"] = pOrder->SessionID;
            data["UserProductInfo"] = gb2312_to_utf8(pOrder->UserProductInfo);
            data["StatusMsg"] = gb2312_to_utf8(pOrder->StatusMsg);
            data["UserForceClose"] = pOrder->UserForceClose;
            data["ActiveUserID"] = gb2312_to_utf8(pOrder->ActiveUserID);
            data["BrokerOrderSeq"] = pOrder->BrokerOrderSeq;
            data["RelativeOrderSysID"] = gb2312_to_utf8(pOrder->RelativeOrderSysID);
            data["ZCETotalTradedVolume"] = pOrder->ZCETotalTradedVolume;
            data["IsSwapOrder"] = pOrder->IsSwapOrder;
            data["BranchID"] = gb2312_to_utf8(pOrder->BranchID);
            data["InvestUnitID"] = gb2312_to_utf8(pOrder->InvestUnitID);
            data["AccountID"] = gb2312_to_utf8(pOrder->AccountID);
            data["CurrencyID"] = gb2312_to_utf8(pOrder->CurrencyID);
            data["MacAddress"] = gb2312_to_utf8(pOrder->MacAddress);
            data["InstrumentID"] = gb2312_to_utf8(pOrder->InstrumentID);
            data["ExchangeInstID"] = gb2312_to_utf8(pOrder->ExchangeInstID);
            data["IPAddress"] = gb2312_to_utf8(pOrder->IPAddress);
        }
        this->PyOnRtnOrder(data);
    });
}

void TdApi::OnRtnTrade(CThostFtdcTradeField *pTrade) {
    queue_->dispatch([&]() {
        py::gil_scoped_acquire acquire;

        py::dict data;
        if (pTrade) {
            data["BrokerID"] = gb2312_to_utf8(pTrade->BrokerID);
            data["InvestorID"] = gb2312_to_utf8(pTrade->InvestorID);
            data["OrderRef"] = gb2312_to_utf8(pTrade->OrderRef);
            data["UserID"] = gb2312_to_utf8(pTrade->UserID);
            data["ExchangeID"] = gb2312_to_utf8(pTrade->ExchangeID);
            data["TradeID"] = gb2312_to_utf8(pTrade->TradeID);
            data["Direction"] = pTrade->Direction;
            data["OrderSysID"] = gb2312_to_utf8(pTrade->OrderSysID);
            data["ParticipantID"] = gb2312_to_utf8(pTrade->ParticipantID);
            data["ClientID"] = gb2312_to_utf8(pTrade->ClientID);
            data["TradingRole"] = pTrade->TradingRole;
            data["OffsetFlag"] = pTrade->OffsetFlag;
            data["HedgeFlag"] = pTrade->HedgeFlag;
            data["Price"] = pTrade->Price;
            data["Volume"] = pTrade->Volume;
            data["TradeDate"] = gb2312_to_utf8(pTrade->TradeDate);
            data["TradeTime"] = gb2312_to_utf8(pTrade->TradeTime);
            data["TradeType"] = pTrade->TradeType;
            data["PriceSource"] = pTrade->PriceSource;
            data["TraderID"] = gb2312_to_utf8(pTrade->TraderID);
            data["OrderLocalID"] = gb2312_to_utf8(pTrade->OrderLocalID);
            data["ClearingPartID"] = gb2312_to_utf8(pTrade->ClearingPartID);
            data["BusinessUnit"] = gb2312_to_utf8(pTrade->BusinessUnit);
            data["SequenceNo"] = pTrade->SequenceNo;
            data["TradingDay"] = gb2312_to_utf8(pTrade->TradingDay);
            data["SettlementID"] = pTrade->SettlementID;
            data["BrokerOrderSeq"] = pTrade->BrokerOrderSeq;
            data["TradeSource"] = pTrade->TradeSource;
            data["InvestUnitID"] = gb2312_to_utf8(pTrade->InvestUnitID);
            data["InstrumentID"] = gb2312_to_utf8(pTrade->InstrumentID);
            data["ExchangeInstID"] = gb2312_to_utf8(pTrade->ExchangeInstID);
        }

        this->PyOnRtnTrade(data);
    });
}
