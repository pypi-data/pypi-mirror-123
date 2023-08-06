SELECT PackImport.timestamp_Creation,
       PackImport.timestamp_Modification,
       PackImport.id_Order,
       PackImport.date_Imported,
       PackImport.Weight,
       PackImport.Cost,
       PackImport.TrackingNumber,
       PackImport.Address1,
       PackImport.Address2,
       PackImport.AddressCity,
       PackImport.AddressCompany,
       PackImport.AddressCountry,
       PackImport.AddressDescription,
       PackImport.AddressState,
       PackImport.AddressZip
FROM PackImport
WHERE PackImport.id_Order = {order_number}
