SELECT LinesOE.ID_LineOE,
       LinesOE.PartNumber,
       LinesOE.PartColorRange,
       LinesOE.PartColor,
       LinesOE.PartDescription,
       LinesOE.Size01_Req,
       LinesOE.Size02_Req,
       LinesOE.Size03_Req,
       LinesOE.Size04_Req,
       LinesOE.Size05_Req,
       LinesOE.Size06_Req,
       LinesOE.cn_LineQuantity_Req,
       LinesOE.id_OrderType,
       LinesOE.OrderInstructions,
       LinesOE.OrderInvoiceNotes,
       LinesOE.cnCur_LinePrice_Req
FROM LinesOE
WHERE LinesOE.id_order = {order_number}
