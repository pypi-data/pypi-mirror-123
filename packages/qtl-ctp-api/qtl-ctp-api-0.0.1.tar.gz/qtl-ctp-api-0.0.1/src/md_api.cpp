#include "md_api.h"


void MdApi::CreateApi(const std::string &flow_path) {
    queue_ = new DispatchQueue();
    api_ = CThostFtdcMdApi::CreateFtdcMdApi(flow_path.c_str());
    api_->RegisterSpi(this);
}

std::string MdApi::GetApiVersion() {
    return CThostFtdcMdApi::GetApiVersion();
}

void MdApi::Release() {
    api_->Release();
    delete queue_;
}

void MdApi::Init() {
    api_->Init();
}

int MdApi::Join() {
    return api_->Join();
}

std::string MdApi::GetTradingDay() {
    return api_->GetTradingDay();
}

void MdApi::RegisterFront(const std::string &front_address) {
    api_->RegisterFront(const_cast<char *>(front_address.c_str()));
}

int MdApi::SubscribeMarketData(const std::string &instrument_id) {
    char *buffer = (char*)instrument_id.c_str();
    char *req[1] = { buffer };
    return api_->SubscribeMarketData(req, 1);
}

int MdApi::UnSubscribeMarketData(const std::string &instrument_id) {
    char *buffer = (char*)instrument_id.c_str();
    char *req[1] = { buffer };
    return api_->UnSubscribeMarketData(req, 1);
}

// Req Methods
int MdApi::ReqUserLogin(const py::dict &data, int request_id) {
    CThostFtdcReqUserLoginField request{};
    strncpy(request.BrokerID, data["BrokerID"].cast<std::string>().c_str(), sizeof(request.BrokerID));
    strncpy(request.UserID, data["UserID"].cast<std::string>().c_str(), sizeof(request.UserID));
    strncpy(request.Password, data["Password"].cast<std::string>().c_str(), sizeof(request.Password));
    return api_->ReqUserLogin(&request, request_id);
}

int MdApi::ReqUserLogout(const py::dict &data, int request_id) {
    CThostFtdcUserLogoutField request{};
    strncpy(request.BrokerID, data["BrokerID"].cast<std::string>().c_str(), sizeof(request.BrokerID));
    strncpy(request.UserID, data["UserID"].cast<std::string>().c_str(), sizeof(request.UserID));
    return api_->ReqUserLogout(&request, request_id);
}

// On Methods
void MdApi::OnFrontConnected() {
    queue_->dispatch([&]() {
        py::gil_scoped_acquire acquire;
        this->PyOnFrontConnected();
    });
}

void MdApi::OnFrontDisconnected(int reason) {
    queue_->dispatch([&]() {
        py::gil_scoped_acquire acquire;
        this->PyOnFrontDisconnected(reason);
    });
}

void MdApi::OnHeartBeatWarning(int time_lapse) {
    queue_->dispatch([&]() {
        py::gil_scoped_acquire acquire;
        this->PyOnHeartBeatWarning(time_lapse);
    });
}

void MdApi::OnRspUserLogin(CThostFtdcRspUserLoginField *pRspUserLogin, CThostFtdcRspInfoField *pRspInfo, int request_id, bool is_last) {
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

void MdApi::OnRspUserLogout(CThostFtdcUserLogoutField *pUserLogout, CThostFtdcRspInfoField *pRspInfo, int request_id, bool is_last) {
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

void MdApi::OnRspError(CThostFtdcRspInfoField *pRspInfo, int request_id, bool is_last) {
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

void MdApi::OnRspSubMarketData(CThostFtdcSpecificInstrumentField *pSpecificInstrument, CThostFtdcRspInfoField *pRspInfo, int request_id, bool is_last) {
    queue_->dispatch([&]() {
        py::gil_scoped_acquire acquire;

        py::dict data;
        if (pSpecificInstrument) {
            data["InstrumentID"] = gb2312_to_utf8(pSpecificInstrument->InstrumentID);
        }

        py::dict error;
        if (pRspInfo) {
            error["ErrorID"] = pRspInfo->ErrorID;
            error["ErrorMsg"] = gb2312_to_utf8(pRspInfo->ErrorMsg);
        }

        this->PyOnRspSubMarketData(data, error, request_id, is_last);
    });
}

void MdApi::OnRspUnSubMarketData(CThostFtdcSpecificInstrumentField *pSpecificInstrument, CThostFtdcRspInfoField *pRspInfo, int request_id, bool is_last) {
    queue_->dispatch([&]() {
        py::gil_scoped_acquire acquire;

        py::dict data;
        if (pSpecificInstrument) {
            data["InstrumentID"] = gb2312_to_utf8(pSpecificInstrument->InstrumentID);
        }

        py::dict error;
        if (pRspInfo) {
            error["ErrorID"] = pRspInfo->ErrorID;
            error["ErrorMsg"] = gb2312_to_utf8(pRspInfo->ErrorMsg);
        }

        this->PyOnRspUnSubMarketData(data, error, request_id, is_last);
    });
}

void MdApi::OnRtnDepthMarketData(CThostFtdcDepthMarketDataField *pDepthMarketData) {
    queue_->dispatch([&]() {
        py::gil_scoped_acquire acquire;

        py::dict data;
        if (pDepthMarketData) {
            data["TradingDay"] = gb2312_to_utf8(pDepthMarketData->TradingDay);
            data["ExchangeID"] = gb2312_to_utf8(pDepthMarketData->ExchangeID);
            data["LastPrice"] = adjust_price(pDepthMarketData->LastPrice);
            data["PreSettlementPrice"] = adjust_price(pDepthMarketData->PreSettlementPrice);
            data["PreClosePrice"] = adjust_price(pDepthMarketData->PreClosePrice);
            data["PreOpenInterest"] = pDepthMarketData->PreOpenInterest;
            data["OpenPrice"] = adjust_price(pDepthMarketData->OpenPrice);
            data["HighestPrice"] = adjust_price(pDepthMarketData->HighestPrice);
            data["LowestPrice"] = adjust_price(pDepthMarketData->LowestPrice);
            data["Volume"] = pDepthMarketData->Volume;
            data["Turnover"] = pDepthMarketData->Turnover;
            data["OpenInterest"] = pDepthMarketData->OpenInterest;
            data["ClosePrice"] = adjust_price(pDepthMarketData->ClosePrice);
            data["SettlementPrice"] = adjust_price(pDepthMarketData->SettlementPrice);
            data["UpperLimitPrice"] = adjust_price(pDepthMarketData->UpperLimitPrice);
            data["LowerLimitPrice"] = adjust_price(pDepthMarketData->LowerLimitPrice);
            data["PreDelta"] = pDepthMarketData->PreDelta;
            data["CurrDelta"] = pDepthMarketData->CurrDelta;
            data["UpdateTime"] = gb2312_to_utf8(pDepthMarketData->UpdateTime);
            data["UpdateMillisec"] = pDepthMarketData->UpdateMillisec;
            data["BidPrice1"] = adjust_price(pDepthMarketData->BidPrice1);
            data["BidVolume1"] = pDepthMarketData->BidVolume1;
            data["AskPrice1"] = adjust_price(pDepthMarketData->AskPrice1);
            data["AskVolume1"] = pDepthMarketData->AskVolume1;
            data["BidPrice2"] = adjust_price(pDepthMarketData->BidPrice2);
            data["BidVolume2"] = pDepthMarketData->BidVolume2;
            data["AskPrice2"] = adjust_price(pDepthMarketData->AskPrice2);
            data["AskVolume2"] = pDepthMarketData->AskVolume2;
            data["BidPrice3"] = adjust_price(pDepthMarketData->BidPrice3);
            data["BidVolume3"] = pDepthMarketData->BidVolume3;
            data["AskPrice3"] = adjust_price(pDepthMarketData->AskPrice3);
            data["AskVolume3"] = pDepthMarketData->AskVolume3;
            data["BidPrice4"] = adjust_price(pDepthMarketData->BidPrice4);
            data["BidVolume4"] = pDepthMarketData->BidVolume4;
            data["AskPrice4"] = adjust_price(pDepthMarketData->AskPrice4);
            data["AskVolume4"] = pDepthMarketData->AskVolume4;
            data["BidPrice5"] = adjust_price(pDepthMarketData->BidPrice5);
            data["BidVolume5"] = pDepthMarketData->BidVolume5;
            data["AskPrice5"] = adjust_price(pDepthMarketData->AskPrice5);
            data["AskVolume5"] = pDepthMarketData->AskVolume5;
            data["AveragePrice"] = adjust_price(pDepthMarketData->AveragePrice);
            data["ActionDay"] = gb2312_to_utf8(pDepthMarketData->ActionDay);
            data["InstrumentID"] = gb2312_to_utf8(pDepthMarketData->InstrumentID);
            data["ExchangeInstID"] = gb2312_to_utf8(pDepthMarketData->ExchangeInstID);
        }

        this->PyOnRtnDepthMarketData(data);
    });
}
