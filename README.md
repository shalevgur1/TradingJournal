# TradingJournal
Trading Journal application for Interactive brokers
This application is designed to help track your trading information and trading history.
This application is mainly for statistics and drawing conclusions from trading history.
The application utilizes Excel Table that is used as the UI.

The application uses Interactive Brokers python API and can operate with both TWS and IBGW (need to be configured)
The implements the following architectures and design:
1. Client Server - The application uses the IB API and implements a client-server SW architecture. The application itself is used as
   the client while the TWS or IBGW is used as the Server (the TWS or IBGW is actually a bridge to the Interactive Brokers remote servers).
2. Multi-Threading - The application utilizes Python Multi-Threading SW architecture to enable concurrent operations.

For more information see the attached charts (Threads chart and SW architecture chart) in the application's folder.

